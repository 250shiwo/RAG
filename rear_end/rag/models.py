from django.db import models
from django.contrib.auth.models import User
import uuid


class ChatHistory(models.Model):
    """聊天历史记录模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    kb_id = models.IntegerField()
    session_id = models.UUIDField(default=uuid.uuid4, editable=False)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    token_usage = models.JSONField(null=True, blank=True)
    elapsed_ms = models.IntegerField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.created_at}"
