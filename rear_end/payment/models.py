from django.db import models
from django.contrib.auth.models import User
from users.models import SubscriptionPlan


class PaymentOrder(models.Model):
    """支付订单模型"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    order_id = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[
        ('pending', '待支付'),
        ('completed', '已完成'),
        ('failed', '失败')
    ], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name} - {self.status}"
