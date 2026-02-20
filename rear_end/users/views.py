from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer


class RegisterView(APIView):
    # 注册不需要鉴权
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)


class LoginView(TokenObtainPairView):
    # 登录接口：返回 JWT token（access/refresh）
    permission_classes = [AllowAny]


class RefreshView(TokenRefreshView):
    permission_classes = [AllowAny]


class MeView(APIView):
    # 鉴权验证接口：必须携带 Bearer access
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data, status=status.HTTP_200_OK)
