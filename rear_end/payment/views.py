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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0I1/K1D5R+/gueCSHYT5R4pofREaQIPWYE97DXJmTkCgYEAihJahel4nE3Ssb9Dg6n+YMtXUOuws+bT4iiNCg+hxxvS3Po2on1++BckjiPY7Z7a8o32osE61I1vsnmvEEiF+U2efxud3jF243Ep8sEF63FNzJWfpY1CIpkPyW6zNb79cOSSMmRG2fODOMgASehi1+vwyYImTMsb7mH40IYnbJcCgYEAp9OxYxudZVwByVxadIMOLGcON5Q0mdjXqBur8OwWnf31e5DUN/bsPWPfpLPrx6Zs205pB3XVwa+nJuEtN+gddYf/9rVdcqqzrDZvCXQ53n4DrL09uWVYc16azfpnO7pUYi+Z5PKvo/c4/swntopZzJwAr6bH9yTq0zSfFq/1rHkCgYAWt6RbSinFFeznv/98x1iKVoqcTts5Dm6oVGG4WRAWMZbFMwoQPDPK4Avssys7FZsSs5bz+nUSid7p76mFNVmNxl6grUuRRnQ4QeNUBLxTm8XgNnIZDB/oj2SQkP09h5otm/4N+n/J1o4tpoKdpnW07yYkEZz5n6WN2GLW9GvCKwKBgQCz/c8HyZrUb7ogA8dCd1b2hgzewspSpxHUNIhZC8qkdh2BGq8vCfvcGdYY8IFL8/mVdV4Xv27gMzW6NsgSi6l8ZPwyejnIxofZOCFliS0musrh/fd7VLhbjCCE245F6KAxE+nnspq/qTWxSD4WexTs6JwYH9o9I8cJRjeMyhUuxQ==import os
importimport os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_frameworkimport os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Responseimport os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay.aop.api.DefaultAlipayClientimport os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel importimport os
import uuid
from datetime import datetime, timedelta
from django.http import HttpResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePagePayModel import AlipayTradePagePayModel
from alipay.aop.api.request.AlipayTradePagePayRequestimport os
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
from users.models importimport os
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
    "import os
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
        plan_id = requestimport os
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
            plan = SubscriptionPlanimport os
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
        exceptimport os
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
            return Response({"detail": "订阅计划不存在"import os
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
        
        # 创建import os
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
            planimport os
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
        )import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  #import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="90210001626import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9wimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1Wimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbWimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5simport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvbimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMovimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyALimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r4import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2eimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsVimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn35import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0import os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0I1/K1D5R+/gueCSimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0I1/K1D5R+/gueCSHYT5R4pofREaQimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0I1/K1D5R+/gueCSHYT5R4pofREaQIPWYE97DXJmTkCgYEAihJahel4nEimport os
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
        
        # 初始化支付宝客户端
        alipay_client = DefaultAlipayClient(
            server_url="https://openapi.alipaydev.com/gateway.do",  # 沙箱环境
            app_id="9021000162684170",
            private_key="MIIEpAIBAAKCAQEAhzycI+R/jis95Sbe5U6Z9w8gcGjZcmZvHOzgrnJbYsPefaQUn2oBp1iuWOtQxobywRvnJ1jBKHaASS+GQFEp+LkFs3MukSFhccIC2OntfgYWUoFwOd8ROcn8m2gGCi7HPfOcNt0y+h1+BMOgcoB/48AvUUilfhvjo1WCRypIM6Jg3BqX8RG0G00CiCOrLziIO4+NbOHfnKu3/WAQK3V18An09akme+oRt9bnuH6TxlC/Qe16/kvgvczdoeGPezt+vFMRMiwOweIZCBHz/5GPiFaRfmIgFUFlkn/yEbW26d3IAeJkRcsOE4GIInd02pdJMDPe1nkvR8pxU5s+9DxsnwIDAQABAoIBAGa0DfRoNMLYbiIYGhDVV7I8B6u2xOTPjDTQZHW3HVXtYIvUT2EdlXHstEONOgP7OmKTeUH1coPzMsvhzrgLq69bfEvi/otzaViGOblYNmeN4ef4qy0YDjHwBupS3rte+StAVfOIm409VpXxp2kt03I4Yvb9D8mtDnzdlJnNL5Yd5N6vZJyL4zKBFvjq3708W0U4WS6ssSW0WBq8NVASg2id7Ms29+maLAlKF4mMov9TnuyFr5zmsy0WWwZKRXFcEjAPlDJTdgcsVL8v45cs9ueS/I52iDkfKZoQCYje/gM4F5oe1ib/a7/I8WWgOlyAL09D5s4dT/5i34qemhJ8mPECgYEA+r5kVrTu72SRfW+UP12J+r42oSYF7gWHm2e/mK2V/md+fpMsV2VwMF7CwO1GWf5hahcH+ihDsiGn4NBZUmJYlvn351UwtsmCq2UVHsH5115UZOxIVhCwuI4QJWGgl6duo0I1/K1D5R+/gueCSHYT5R4pofREaQIPWYE97DXJmTkCgYEAihJahel4nE3Ssb9Dg6n+YMtXUOuws+bT4iiNC