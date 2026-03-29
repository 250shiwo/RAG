from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import StreamingHttpResponse

from knowledge.models import KnowledgeBase

from .serializers import RagChatRequestSerializer
from .services import RagError, rag_chat, rag_chat_stream


class RagChatView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RagChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kb_id = serializer.validated_data["kb_id"]
        question = serializer.validated_data["question"]

        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            payload = rag_chat(kb, question)
        except RagError as e:
            return Response({"detail": e.detail}, status=e.status_code)

        return Response(payload, status=status.HTTP_200_OK)


class RagChatStreamView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = RagChatRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        kb_id = serializer.validated_data["kb_id"]
        question = serializer.validated_data["question"]

        kb = KnowledgeBase.objects.filter(id=kb_id, user=request.user).first()
        if kb is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            stream = rag_chat_stream(kb, question)
        except RagError as e:
            return Response({"detail": e.detail}, status=e.status_code)

        def gen():
            for delta in stream:
                yield (delta or "").encode("utf-8", errors="ignore")

        resp = StreamingHttpResponse(gen(), content_type="text/plain; charset=utf-8")
        resp["Cache-Control"] = "no-cache"
        resp["X-Accel-Buffering"] = "no"
        return resp
