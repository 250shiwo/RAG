from django.urls import path

from .views import LoginView, MeView, RefreshView, RegisterView, ChangePasswordView
from .subscription_views import SubscriptionPlanListView, UserSubscriptionView, UserUsageView, SubscribeView

urlpatterns = [
    path("register", RegisterView.as_view(), name="register"),
    path("login", LoginView.as_view(), name="login"),
    path("refresh", RefreshView.as_view(), name="refresh"),
    path("me", MeView.as_view(), name="me"),
    path("change-password", ChangePasswordView.as_view(), name="change-password"),
    # 订阅相关API
    path("subscriptions/plans", SubscriptionPlanListView.as_view(), name="subscription-plans"),
    path("subscriptions/me", UserSubscriptionView.as_view(), name="user-subscription"),
    path("subscriptions/usage", UserUsageView.as_view(), name="user-usage"),
    path("subscriptions/subscribe", SubscribeView.as_view(), name="subscribe"),
]
