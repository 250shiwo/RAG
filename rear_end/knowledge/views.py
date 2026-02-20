import uuid
from pathlib import Path

from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Document, DocumentChunk, KnowledgeBase
from .serializers import (
    DocumentUploadSerializer,
    KnowledgeBaseCreateSerializer,
    KnowledgeBaseSerializer,
)
from .services import (
    build_kb_index_path,
    build_upload_path,
    create_empty_index_file,
    safe_remove_file,
    save_uploaded_file,
)
from .vectorstore import add_vectors_to_index, chunk_text, rebuild_index


class KnowledgeBaseCreateView(APIView):
    # 创建知识库：必须登录
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = KnowledgeBaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            kb = KnowledgeBase.objects.create(
                user=request.user,
                name=serializer.validated_data["name"],
                description=serializer.validated_data.get("description", ""),
                faiss_path="",
            )

            index_path = build_kb_index_path(user_id=request.user.id, kb_id=kb.id)
            kb.faiss_path = str(index_path.resolve())
            kb.save(update_fields=["faiss_path"])

            try:
                create_empty_index_file(index_path)
            except Exception:
                KnowledgeBase.objects.filter(id=kb.id).delete()
                raise

        return Response(KnowledgeBaseSerializer(kb).data, status=status.HTTP_201_CREATED)


class KnowledgeBaseListView(APIView):
    # 获取我的知识库列表：必须登录
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = KnowledgeBase.objects.filter(user=request.user).order_by("-created_at")
        return Response({"items": KnowledgeBaseSerializer(items, many=True).data})


class KnowledgeBaseDeleteView(APIView):
    # 删除知识库：必须登录，只能删除自己的资源
    permission_classes = [IsAuthenticated]

    def delete(self, request, kb_id: int):
        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        faiss_path = kb.faiss_path
        kb.delete()
        if faiss_path:
            safe_remove_file(faiss_path)

        return Response(status=status.HTTP_204_NO_CONTENT)


class KnowledgeBaseUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DocumentUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kb_id = serializer.validated_data["kb_id"]
        on_conflict = serializer.validated_data["on_conflict"]
        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        file_obj = serializer.validated_data["file"]
        original_name = Path(file_obj.name).name
        existing = Document.objects.filter(kb=kb, filename=original_name)
        has_conflict = existing.exists()

        filename = original_name
        if has_conflict and on_conflict == "keep":
            suffix = Path(original_name).suffix
            while True:
                candidate = f"{uuid.uuid4().hex}{suffix}"
                if not Document.objects.filter(kb=kb, filename=candidate).exists():
                    filename = candidate
                    break

        upload_path = build_upload_path(request.user.id, kb.id, filename)
        save_uploaded_file(upload_path, file_obj)

        # 当前最小实现：将上传文件按文本读取（优先 utf-8，失败回退 gbk）。
        raw = upload_path.read_bytes()
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = raw.decode("gbk", errors="ignore")

        # 分块：后续 RAG 检索/重建索引都以 chunk 为最小单元。
        chunks = chunk_text(text)
        if not chunks:
            safe_remove_file(upload_path)
            return Response({"detail": "文件无可用文本内容"}, status=status.HTTP_400_BAD_REQUEST)

        removed_files: list[str] = []

        # 先写入数据库（Document + Chunk），保证后续可重建索引。
        with transaction.atomic():
            if has_conflict and on_conflict == "replace":
                removed_files = [
                    fp for fp in existing.values_list("file_path", flat=True) if fp
                ]
                existing.delete()

            doc = Document.objects.create(
                kb=kb,
                filename=filename,
                file_path=str(upload_path.resolve()),
                chunk_count=len(chunks),
            )
            DocumentChunk.objects.bulk_create(
                [DocumentChunk(document=doc, chunk_index=i, text=t) for i, t in enumerate(chunks)]
            )

        faiss_path = Path(kb.faiss_path)
        if has_conflict and on_conflict == "replace":
            for fp in removed_files:
                safe_remove_file(fp)

            remaining_texts = DocumentChunk.objects.filter(document__kb=kb).order_by(
                "document_id", "chunk_index"
            ).values_list("text", flat=True)
            rebuild_index(faiss_path, remaining_texts)
        else:
            # 向量写入 FAISS：写入到该知识库的 kb.faiss_path。
            added = add_vectors_to_index(faiss_path, chunks)
            if added != len(chunks):
                return Response({"detail": "向量写入失败"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(
            {
                "id": doc.id,
                "kb_id": kb.id,
                "filename": doc.filename,
                "chunk_count": doc.chunk_count,
                "uploaded_at": doc.uploaded_at,
            },
            status=status.HTTP_201_CREATED,
        )


class KnowledgeBaseDocumentsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, kb_id: int):
        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        docs = Document.objects.filter(kb=kb).order_by("-uploaded_at")
        items = [
            {
                "id": d.id,
                "filename": d.filename,
                "chunk_count": d.chunk_count,
                "uploaded_at": d.uploaded_at,
            }
            for d in docs
        ]
        return Response({"items": items}, status=status.HTTP_200_OK)


class DocumentDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, doc_id: int):
        doc = Document.objects.select_related("kb").filter(id=doc_id, kb__user=request.user).first()
        if doc is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kb = doc.kb
        faiss_path = kb.faiss_path
        file_path = doc.file_path

        doc.delete()

        if file_path:
            safe_remove_file(file_path)

        # 删除文档后通过“重建索引”保持 FAISS 与数据库一致。
        remaining_texts = DocumentChunk.objects.filter(document__kb=kb).order_by(
            "document_id", "chunk_index"
        ).values_list("text", flat=True)
        rebuild_index(Path(faiss_path), remaining_texts)

        return Response(status=status.HTTP_204_NO_CONTENT)
