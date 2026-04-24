from rest_framework import serializers
import uuid


class RagChatRequestSerializer(serializers.Serializer):
    kb_id = serializers.IntegerField()
    question = serializers.CharField(allow_blank=False, trim_whitespace=True)
    session_id = serializers.UUIDField(required=False, default=uuid.uuid4)


class RagChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(allow_blank=False)
    elapsed_ms = serializers.IntegerField()
    token_usage = serializers.DictField()
    session_id = serializers.UUIDField()
