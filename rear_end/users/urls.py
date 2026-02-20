from django.urls import path

from .views import LoginView, MeView, RefreshView, RegisterView

urlpatterns = [
    path("register", RegisterView.as_view(), name="users-register"),
    path("login", LoginView.as_view(), name="users-login"),
    path("refresh", RefreshView.as_view(), name="users-refresh"),
    path("me", MeView.as_view(), name="users-me"),
]
