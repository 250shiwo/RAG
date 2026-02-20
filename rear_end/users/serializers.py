from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    # 仅返回安全字段：避免泄露密码、权限等敏感信息
    class Meta:
        model = User
        fields = ("id", "username", "email")


class RegisterSerializer(serializers.Serializer):
    # 注册接口输入字段：password 仅写入，不回显
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField(required=False, allow_null=True, allow_blank=True)

    def validate_username(self, value: str) -> str:
        # 用户名唯一性校验（避免直接触发数据库完整性异常）
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("用户名已存在")
        return value

    def validate_password(self, value: str) -> str:
        # 复用 Django 内置密码规则（settings.py 的 AUTH_PASSWORD_VALIDATORS）
        validate_password(value)
        return value

    def create(self, validated_data):
        # create_user 会自动做 password hash
        username = validated_data["username"]
        password = validated_data["password"]
        email = validated_data.get("email") or ""
        return User.objects.create_user(username=username, password=password, email=email)
