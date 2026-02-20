from django.conf import settings
from django.db import models


class KnowledgeBase(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    faiss_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.name


class Document(models.Model):
    kb = models.ForeignKey(KnowledgeBase, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    file_path = models.CharField(max_length=500, blank=True)
    chunk_count = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.filename


class DocumentChunk(models.Model):
    document = models.ForeignKey(Document, on_delete=models.CASCADE, related_name="chunks")
    chunk_index = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ("document", "chunk_index")
