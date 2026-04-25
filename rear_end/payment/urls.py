from django.urls import path

from .views import AliPayView, AliPayNotifyView, AliPayReturnView

urlpatterns = [
    path("alipay", AliPayView.as_view(), name="alipay"),
    path("notify", AliPayNotifyView.as_view(), name="alipay-notify"),
    path("return", AliPayReturnView.as_view(), name="alipay-return"),
]
