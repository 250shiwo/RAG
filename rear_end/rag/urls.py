from django.urls import path

from .views import RagChatView, RagChatStreamView
from .history_views import ChatHistoryView

urlpatterns = [
    path("chat", RagChatView.as_view(), name="rag-chat"),
    path("chat/stream", RagChatStreamView.as_view(), name="rag-chat-stream"),
    path("history", ChatHistoryView.as_view(), name="chat-history"),
    path("history/<int:history_id>", ChatHistoryView.as_view(), name="chat-history-detail"),
]
