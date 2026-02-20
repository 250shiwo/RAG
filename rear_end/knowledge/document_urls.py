from django.urls import path

from .views import DocumentDeleteView

urlpatterns = [
    path("<int:doc_id>", DocumentDeleteView.as_view(), name="document-delete"),
]
