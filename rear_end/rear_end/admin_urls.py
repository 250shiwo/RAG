from django.urls import path

from .admin_views import (
    AdminDocumentDetailView,
    AdminKnowledgeBaseDetailView,
    AdminKnowledgeBaseDocumentsView,
    AdminKnowledgeBasesView,
    AdminUserDetailView,
    AdminUsersView,
)

urlpatterns = [
    path("users", AdminUsersView.as_view()),
    path("users/<int:user_id>", AdminUserDetailView.as_view()),
    path("kb", AdminKnowledgeBasesView.as_view()),
    path("kb/<int:kb_id>", AdminKnowledgeBaseDetailView.as_view()),
    path("kb/<int:kb_id>/documents", AdminKnowledgeBaseDocumentsView.as_view()),
    path("document/<int:doc_id>", AdminDocumentDetailView.as_view()),
]

