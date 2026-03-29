from rest_framework import serializers


class RagChatRequestSerializer(serializers.Serializer):
    kb_id = serializers.IntegerField()
    question = serializers.CharField(allow_blank=False, trim_whitespace=True)


class RagChatResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(allow_blank=False)
    elapsed_ms = serializers.IntegerField()
    token_usage = serializers.DictField()
