from django.urls import path

from .views import RagChatStreamView, RagChatView

urlpatterns = [
    path("chat", RagChatView.as_view(), name="rag-chat"),
    path("chat/stream", RagChatStreamView.as_view(), name="rag-chat-stream"),
]
