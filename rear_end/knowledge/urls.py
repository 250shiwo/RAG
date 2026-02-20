from django.urls import path

from .views import (
    KnowledgeBaseCreateView,
    KnowledgeBaseDeleteView,
    KnowledgeBaseDocumentsView,
    KnowledgeBaseListView,
    KnowledgeBaseUploadView,
)

urlpatterns = [
    path("create", KnowledgeBaseCreateView.as_view(), name="kb-create"),
    path("list", KnowledgeBaseListView.as_view(), name="kb-list"),
    path("upload", KnowledgeBaseUploadView.as_view(), name="kb-upload"),
    path("<int:kb_id>/documents", KnowledgeBaseDocumentsView.as_view(), name="kb-documents"),
    path("<int:kb_id>", KnowledgeBaseDeleteView.as_view(), name="kb-delete"),
]
