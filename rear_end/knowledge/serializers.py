from rest_framework import serializers

from .models import Document, DocumentChunk, KnowledgeBase


class KnowledgeBaseSerializer(serializers.ModelSerializer):
    # 统一对外返回字段
    class Meta:
        model = KnowledgeBase
        fields = ("id", "name", "description", "faiss_path", "created_at")


class KnowledgeBaseCreateSerializer(serializers.ModelSerializer):
    # 创建接口只允许写入 name/description
    class Meta:
        model = KnowledgeBase
        fields = ("name", "description")


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ("id", "kb", "filename", "chunk_count", "uploaded_at")
        read_only_fields = fields


class DocumentUploadSerializer(serializers.Serializer):
    kb_id = serializers.IntegerField()
    file = serializers.FileField()
    on_conflict = serializers.ChoiceField(choices=("keep", "replace"), required=False, default="keep")

    # 上传文件类型白名单：后端兜底校验，避免不可解析的文件进入入库流程
    ALLOWED_SUFFIXES = {".txt", ".md", ".pdf"}

    def validate_file(self, file_obj):
        # 仅按文件后缀做基础校验；PDF 真伪会在落盘后通过文件头进一步校验
        suffix = (getattr(file_obj, "name", "") or "").strip()
        suffix = (suffix.rsplit(".", 1)[-1] if "." in suffix else "").lower()
        suffix = f".{suffix}" if suffix else ""
        if suffix not in self.ALLOWED_SUFFIXES:
            raise serializers.ValidationError("仅支持上传 .txt / .md / .pdf 文件")
        return file_obj


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ("id", "document", "chunk_index", "text")
