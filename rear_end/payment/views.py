import os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequest import AlipayTradePagePayRequest

from .models import PaymentOrder
from users.models import SubscriptionPlan, UserSubscription


class AliPayView(APIView):
    """支付宝支付接口"""
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """创建支付订单并生成支付链接"""
        plan_id = request.data.get('plan_id')
        
        try:
            plan = SubscriptionPlan.objects.get(id=plan_id)
        except SubscriptionPlan.DoesNotExist:
            return Response({"detail": "订阅计划不存在"}, status=status.HTTP_404_NOT_FOUND)
        
        # 创建订单
        order_id = f"{uuid.uuid4().hex[:16]}"
        order = PaymentOrder.objects.create(
            user=request.user,
            plan=plan,
            order_id=order_id,
            amount=plan.price
        )
        
        # 从环境变量读取支付宝配置
        app_id = os.getenv('ALIPAY_APP_ID')
        private_key = os.getenv('ALIPAY_PRIVATE_KEY')
        public_key = os.getenv('ALIPAY_PUBLIC_KEY')
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id=app_id,
            private_key=private_key,
            alipay_public_key=public_key,
            charset="UTF-8",
            sign_type="RSA2"
        )
        
        # 创建支付模型
        model = AlipayTradePagePayModel()
        model.out_trade_no = order_id
        model.total_amount = str(plan.price)
        model.subject = f"订阅{plan.name}"
        model.product_code = "FAST_INSTANT_TRADE_PAY"
        
        # 创建支付请求
        alipay_request = AlipayTradePagePayRequest()
        alipay_request.set_return_url("http://localhost:5173/subscription")
        alipay_request.set_notify_url("http://localhost:8000/api/payment/notify")
        alipay_request.set_biz_model(model)
        
        # 生成支付链接
        pay_url = alipay_client.page_execute(alipay_request, http_method="GET")
        
        return Response({"pay_url": pay_url, "order_id": order_id})


class AliPayNotifyView(APIView):
    """支付宝异步通知接口"""
    
    def post(self, request):
        """处理支付宝异步通知"""
        # 从环境变量读取支付宝配置
        app_id = os.getenv('ALIPAY_APP_ID')
        private_key = os.getenv('ALIPAY_PRIVATE_KEY')
        public_key = os.getenv('ALIPAY_PUBLIC_KEY')
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",
            app_id=app_id,
            private_key=private_key,
            alipay_public_key=public_key,
            charset="UTF-8",
            sign_type="RSA2"
        )
        
        # 获取通知数据
        data = request.POST.dict()
        
        # 验证通知
        if alipay_client.verify_notify(data):
            # 处理支付成功
            out_trade_no = data.get('out_trade_no')
            trade_status = data.get('trade_status')
            
            if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                # 更新订单状态
                try:
                    order = PaymentOrder.objects.get(order_id=out_trade_no)
                    if order.status == 'pending':
                        order.status = 'completed'
                        order.paid_at = datetime.now()
                        order.save()
                        
                        # 更新用户订阅
                        subscription, created = UserSubscription.objects.get_or_create(user=order.user)
                        subscription.plan = order.plan
                        subscription.start_date = datetime.now()
                        subscription.end_date = datetime.now() + timedelta(days=30)
                        subscription.is_active = True
                        subscription.save()
                except PaymentOrder.DoesNotExist:
                    pass
            
            return HttpResponse('success')
        else:
            return HttpResponse('fail')
