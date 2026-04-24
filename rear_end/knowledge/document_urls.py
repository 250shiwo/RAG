from django.urls import path

from .views import DocumentDeleteView, DocumentPreviewView

urlpatterns = [
    path("<int:doc_id>", DocumentDeleteView.as_view(), name="document-delete"),
    path("<int:doc_id>/preview", DocumentPreviewView.as_view(), name="document-preview"),
]
