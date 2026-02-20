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


class DocumentChunkSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentChunk
        fields = ("id", "document", "chunk_index", "text")
