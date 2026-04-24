from django.db import models
from django.contrib.auth.models import User
from datetime import date


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    monthly_fee = models.BooleanField(default=True)
    daily_chat_limit = models.IntegerField()
    max_knowledge_bases = models.IntegerField()
    
    def __str__(self):
        return f"{self.name} - ¥{self.price}/{('月' if self.monthly_fee else '次')}"


class UserSubscription(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.plan.name if self.plan else '免费版'}"


class UserUsage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=date.today)
    chat_count = models.IntegerField(default=0)
    
    class Meta:
        unique_together = ('user', 'date')
    
    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.chat_count}次"

