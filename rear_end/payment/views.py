import os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.shortcuts import redirect
from urllib.parse import urlencode
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay import AliPay

from .models import PaymentOrder
from users.models import SubscriptionPlan, UserSubscription


def normalize_pem_key(key_content, key_type):
    """兼容 .env 中仅保存密钥正文的场景，自动补全 PEM 头尾。"""
    if not key_content:
        return key_content

    normalized = key_content.strip().replace('\r', '').replace('\n', '')
    if 'BEGIN' in normalized and 'END' in normalized:
        return key_content.strip()

    if key_type == 'private':
        header = '-----BEGIN RSA PRIVATE KEY-----'
        footer = '-----END RSA PRIVATE KEY-----'
    else:
        header = '-----BEGIN PUBLIC KEY-----'
        footer = '-----END PUBLIC KEY-----'

    lines = [normalized[i:i + 64] for i in range(0, len(normalized), 64)]
    return '\n'.join([header, *lines, footer])


def build_alipay_client():
    """按 python-alipay-sdk 构造客户端。"""
    app_id = os.getenv('ALIPAY_APP_ID')
    private_key = os.getenv('ALIPAY_PRIVATE_KEY')
    public_key = os.getenv('ALIPAY_PUBLIC_KEY')
    debug = os.getenv('ALIPAY_DEBUG', 'true').strip().lower() in ('1', 'true', 'yes', 'on')

    if not app_id or not private_key or not public_key:
        raise ValueError('支付宝配置不完整，请检查 ALIPAY_APP_ID / ALIPAY_PRIVATE_KEY / ALIPAY_PUBLIC_KEY')

    return AliPay(
        appid=app_id,
        app_notify_url=None,
        app_private_key_string=normalize_pem_key(private_key, 'private'),
        alipay_public_key_string=normalize_pem_key(public_key, 'public'),
        sign_type='RSA2',
        debug=debug,
    )


def get_payment_urls():
    """统一读取支付回调地址，便于本地开发时通过公网域名回调。"""
    public_base_url = os.getenv('PUBLIC_BASE_URL', '').rstrip('/')
    notify_url = os.getenv('ALIPAY_NOTIFY_URL', '').strip()
    return_url = os.getenv('ALIPAY_RETURN_URL', '').strip()

    if not notify_url and public_base_url:
        notify_url = f"{public_base_url}/api/payment/notify"
    if not return_url and public_base_url:
        return_url = f"{public_base_url}/api/payment/return"

    if not notify_url:
        notify_url = "http://localhost:8000/api/payment/notify"
    if not return_url:
        return_url = "http://localhost:8000/api/payment/return"

    return notify_url, return_url


def build_payment_page_url(alipay_client, order_string):
    """拼接支付页完整地址。"""
    return f"{alipay_client._gateway}?{order_string}"


def get_trade_status(alipay_client, out_trade_no):
    """向支付宝主动查询订单状态，兼容同步回跳缺少 trade_status 的场景。"""
    if not out_trade_no:
        return ''

    try:
        result = alipay_client.api_alipay_trade_query(out_trade_no=out_trade_no)
    except Exception:
        return ''

    if isinstance(result, dict):
        return (result.get('trade_status') or '').strip()
    return ''


def activate_user_subscription(order):
    """订单支付成功后，统一更新订单和订阅状态。"""
    if order.status != 'pending':
        return

    order.status = 'completed'
    order.paid_at = datetime.now()
    order.save()

    subscription, created = UserSubscription.objects.get_or_create(user=order.user)
    subscription.plan = order.plan
    subscription.start_date = datetime.now()
    subscription.end_date = datetime.now() + timedelta(days=30)
    subscription.is_active = True
    subscription.save()


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
        
        try:
            # 当前安装的 SDK 需要先构造 AlipayClientConfig，再初始化客户端。
            alipay_client = build_alipay_client()
        except ValueError as error:
            return Response({"detail": str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        notify_url, return_url = get_payment_urls()
        # 生成签名后的查询串，再拼成完整支付链接。
        order_string = alipay_client.api_alipay_trade_page_pay(
            subject=f"订阅{plan.name}",
            out_trade_no=order_id,
            total_amount=str(plan.price),
            return_url=return_url,
            notify_url=notify_url,
        )
        pay_url = build_payment_page_url(alipay_client, order_string)
        
        # 同时把支付链接放到响应头，便于前端在个别浏览器/代理响应体异常时兜底读取。
        return Response(
            {"pay_url": pay_url, "order_id": order_id},
            headers={
                "X-Pay-Url": pay_url,
                "X-Order-Id": order_id,
            },
        )


class AliPayNotifyView(APIView):
    """支付宝异步通知接口"""
    
    def post(self, request):
        """处理支付宝异步通知"""
        try:
            alipay_client = build_alipay_client()
        except ValueError:
            return HttpResponse('fail')
        
        # 获取通知数据
        data = request.POST.dict() or request.data.dict()
        signature = data.pop('sign', '')
        
        # 验证通知
        if signature and alipay_client.verify(data.copy(), signature):
            # 处理支付成功
            out_trade_no = data.get('out_trade_no')
            trade_status = data.get('trade_status')
            
            if trade_status == 'TRADE_SUCCESS' or trade_status == 'TRADE_FINISHED':
                # 更新订单状态
                try:
                    order = PaymentOrder.objects.get(order_id=out_trade_no)
                    activate_user_subscription(order)
                except PaymentOrder.DoesNotExist:
                    pass
            
            return HttpResponse('success')
        else:
            return HttpResponse('fail')


class AliPayReturnView(APIView):
    """支付宝同步跳转接口，统一回跳到前端订阅页。"""

    def get(self, request):
        paid = False
        order_id = ''

        try:
            alipay_client = build_alipay_client()
        except ValueError:
            alipay_client = None

        data = request.GET.dict()
        signature = data.pop('sign', '')

        # 某些本地开发场景下异步通知可能收不到，这里在同步回跳时补做一次状态落库。
        if alipay_client and signature and alipay_client.verify(data.copy(), signature):
            out_trade_no = data.get('out_trade_no')
            # 页面同步回跳通常不稳定，部分场景不会直接返回 trade_status，这里主动补查一次。
            trade_status = data.get('trade_status') or get_trade_status(alipay_client, out_trade_no)
            if out_trade_no and trade_status in ('TRADE_SUCCESS', 'TRADE_FINISHED'):
                try:
                    order = PaymentOrder.objects.get(order_id=out_trade_no)
                    activate_user_subscription(order)
                    paid = True
                    order_id = out_trade_no
                except PaymentOrder.DoesNotExist:
                    pass

        frontend_url = os.getenv('FRONTEND_SUBSCRIPTION_URL', 'http://localhost:5173/subscription')
        if paid:
            query_string = urlencode({'paid': '1', 'order_id': order_id})
            joiner = '&' if '?' in frontend_url else '?'
            frontend_url = f'{frontend_url}{joiner}{query_string}'
        return redirect(frontend_url)
