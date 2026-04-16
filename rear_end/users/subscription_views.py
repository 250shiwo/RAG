from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from datetime import date, timedelta

from .models import SubscriptionPlan, UserSubscription, UserUsage
from .serializers import SubscriptionPlanSerializer, UserSubscriptionSerializer


class SubscriptionPlanListView(APIView):
    # 获取所有订阅计划
    def get(self, request):
        plans = SubscriptionPlan.objects.all()
        return Response(SubscriptionPlanSerializer(plans, many=True).data)


class UserSubscriptionView(APIView):
    # 获取用户订阅信息
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            return Response(UserSubscriptionSerializer(subscription).data)
        except UserSubscription.DoesNotExist:
            # 返回免费版信息
            return Response({
                "plan": None,
                "is_active": False,
                "daily_chat_limit": 5,
                "max_knowledge_bases": 1
            })


class UserUsageView(APIView):
    # 获取用户今日使用情况
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = date.today()
        usage, created = UserUsage.objects.get_or_create(user=request.user, date=today)
        
        # 获取用户的每日聊天限制
        try:
            subscription = UserSubscription.objects.get(user=request.user)
            if subscription.is_active:
                daily_limit = subscription.plan.daily_chat_limit
            else:
                daily_limit = 5  # 免费版默认5次
        except UserSubscription.DoesNotExist:
            daily_limit = 5  # 免费版默认5次
        
        return Response({
            "chat_count": usage.chat_count,
            "daily_limit": daily_limit,
            "remaining": max(0, daily_limit - usage.chat_count)
        })


class SubscribeView(APIView):
    # 订阅某个计划
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        plan_id = request.data.get('plan_id')
        
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"detail": "订阅计划不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 创建或更新用户订阅
        subscription, created = UserSubscription.objects.get_or_create(user=request.user)
        subscription.plan = plan
        subscription.start_date = date.today()
        subscription.end_date = date.today() + timedelta(days=30)  # 假设按月订阅
        subscription.is_active = True
        subscription.save()
        
        return Response(UserSubscriptionSerializer(subscription).data, status=status.HTTP_201_CREATED)
