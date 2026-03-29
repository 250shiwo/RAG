from pathlib import Path

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.db import transaction
from django.db.models import Q
from rest_framework import serializers
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from knowledge.models import Document, DocumentChunk, KnowledgeBase
from knowledge.services import build_kb_index_path, create_empty_index_file, safe_remove_file
from knowledge.vectorstore import rebuild_index

User = get_user_model()


def _parse_bool_param(raw: str | None):
    if raw is None:
        return None
    v = (raw or "").strip().lower()
    if v in {"1", "true", "yes"}:
        return True
    if v in {"0", "false", "no"}:
        return False
    return "invalid"


def _serialize_user(u):
    return {
        "id": u.id,
        "username": u.username,
        "email": u.email or "",
        "is_active": bool(getattr(u, "is_active", True)),
        "is_staff": bool(getattr(u, "is_staff", False)),
        "date_joined": getattr(u, "date_joined", None),
    }


class AdminUserCreateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    is_active = serializers.BooleanField(required=False, default=True)
    is_staff = serializers.BooleanField(required=False, default=False)

    def validate_username(self, value: str) -> str:
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value


class AdminUserUpdateSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=False)
    password = serializers.CharField(write_only=True, required=False)
    email = serializers.EmailField(required=False, allow_blank=True, allow_null=True)
    is_active = serializers.BooleanField(required=False)
    is_staff = serializers.BooleanField(required=False)

    def validate_username(self, value: str) -> str:
        user = self.context.get("user")
        qs = User.objects.filter(username=value)
        if user is not None:
            qs = qs.exclude(id=getattr(user, "id", None))
        if qs.exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_password(self, value: str) -> str:
        validate_password(value)
        return value


class AdminKnowledgeBaseCreateSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    name = serializers.CharField(max_length=100)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class AdminKnowledgeBaseUpdateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100, required=False)
    description = serializers.CharField(required=False, allow_blank=True, allow_null=True)


class AdminBaseView(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]


class AdminUsersView(AdminBaseView):
    def get(self, request):
        q = (request.query_params.get("q") or "").strip()
        is_active = _parse_bool_param(request.query_params.get("is_active"))
        if is_active == "invalid":
            return Response({"detail": "is_active 参数非法"}, status=status.HTTP_400_BAD_REQUEST)

        users = User.objects.all().order_by("-date_joined", "-id")
        if q:
            users = users.filter(Q(username__icontains=q) | Q(email__icontains=q))
        if is_active is not None:
            users = users.filter(is_active=bool(is_active))

        return Response({"items": [_serialize_user(u) for u in users]}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user = User.objects.create_user(
            username=data["username"],
            password=data["password"],
            email=(data.get("email") or ""),
        )
        user.is_active = bool(data.get("is_active", True))
        user.is_staff = bool(data.get("is_staff", False))
        user.save(update_fields=["is_active", "is_staff"])

        return Response(_serialize_user(user), status=status.HTTP_201_CREATED)


class AdminUserDetailView(AdminBaseView):
    def patch(self, request, user_id: int):
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdminUserUpdateSerializer(data=request.data, context={"user": user}, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        update_fields: list[str] = []
        if "username" in data:
            user.username = data["username"]
            update_fields.append("username")
        if "email" in data:
            user.email = data.get("email") or ""
            update_fields.append("email")
        if "is_active" in data:
            user.is_active = bool(data["is_active"])
            update_fields.append("is_active")
        if "is_staff" in data:
            user.is_staff = bool(data["is_staff"])
            update_fields.append("is_staff")
        if "password" in data:
            user.set_password(data["password"])
            update_fields.append("password")

        if update_fields:
            user.save(update_fields=update_fields)

        return Response(_serialize_user(user), status=status.HTTP_200_OK)

    def delete(self, request, user_id: int):
        user = User.objects.filter(id=user_id).first()
        if user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminKnowledgeBasesView(AdminBaseView):
    def get(self, request):
        user_id_raw = (request.query_params.get("user_id") or "").strip()
        qs = KnowledgeBase.objects.all().order_by("-created_at", "-id")
        if user_id_raw:
            try:
                user_id = int(user_id_raw)
            except Exception:
                return Response({"detail": "user_id 参数非法"}, status=status.HTTP_400_BAD_REQUEST)
            qs = qs.filter(user_id=user_id)

        items = [
            {
                "id": kb.id,
                "user_id": kb.user_id,
                "name": kb.name,
                "description": kb.description,
                "faiss_path": kb.faiss_path,
                "created_at": kb.created_at,
            }
            for kb in qs
        ]
        return Response({"items": items}, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = AdminKnowledgeBaseCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        target_user = User.objects.filter(id=data["user_id"]).first()
        if target_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        with transaction.atomic():
            kb = KnowledgeBase.objects.create(
                user=target_user,
                name=data["name"],
                description=data.get("description") or "",
                faiss_path="",
            )

            index_path = build_kb_index_path(user_id=target_user.id, kb_id=kb.id)
            kb.faiss_path = str(index_path.resolve())
            kb.save(update_fields=["faiss_path"])

            try:
                create_empty_index_file(index_path)
            except Exception:
                KnowledgeBase.objects.filter(id=kb.id).delete()
                raise

        return Response(
            {
                "id": kb.id,
                "user_id": kb.user_id,
                "name": kb.name,
                "description": kb.description,
                "faiss_path": kb.faiss_path,
                "created_at": kb.created_at,
            },
            status=status.HTTP_201_CREATED,
        )


class AdminKnowledgeBaseDetailView(AdminBaseView):
    def patch(self, request, kb_id: int):
        kb = KnowledgeBase.objects.filter(id=kb_id).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = AdminKnowledgeBaseUpdateSerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        update_fields: list[str] = []
        if "name" in data:
            kb.name = data["name"]
            update_fields.append("name")
        if "description" in data:
            kb.description = data.get("description") or ""
            update_fields.append("description")
        if update_fields:
            kb.save(update_fields=update_fields)

        return Response(
            {
                "id": kb.id,
                "user_id": kb.user_id,
                "name": kb.name,
                "description": kb.description,
                "faiss_path": kb.faiss_path,
                "created_at": kb.created_at,
            },
            status=status.HTTP_200_OK,
        )

    def delete(self, request, kb_id: int):
        kb = KnowledgeBase.objects.filter(id=kb_id).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        faiss_path = kb.faiss_path
        kb.delete()
        if faiss_path:
            safe_remove_file(faiss_path)

        return Response(status=status.HTTP_204_NO_CONTENT)


class AdminKnowledgeBaseDocumentsView(AdminBaseView):
    def get(self, request, kb_id: int):
        kb = KnowledgeBase.objects.filter(id=kb_id).first()
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


class AdminDocumentDetailView(AdminBaseView):
    def delete(self, request, doc_id: int):
        doc = Document.objects.select_related("kb").filter(id=doc_id).first()
        if doc is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        kb = doc.kb
        faiss_path = kb.faiss_path
        file_path = doc.file_path

        doc.delete()

        if file_path:
            safe_remove_file(file_path)

        remaining_ids = DocumentChunk.objects.filter(document__kb=kb).order_by(
            "document_id", "chunk_index"
        ).values_list("id", flat=True)
        remaining_texts = DocumentChunk.objects.filter(document__kb=kb).order_by(
            "document_id", "chunk_index"
        ).values_list("text", flat=True)
        rebuild_index(Path(faiss_path), remaining_texts, chunk_ids=remaining_ids)

        return Response(status=status.HTTP_204_NO_CONTENT)
