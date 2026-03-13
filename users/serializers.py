from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer):
    """
    用户序列化器
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'nickname', 'avatar', 'phone', 'email', 'is_active', 'create_time']

class LoginSerializer(serializers.Serializer):
    """
    登录序列化器
    """
    username = serializers.CharField(required=True, label='用户名')
    password = serializers.CharField(required=True, label='密码', write_only=True)

class RegisterSerializer(serializers.ModelSerializer):
    """
    注册序列化器
    """
    password = serializers.CharField(required=True, label='密码', write_only=True)
    password2 = serializers.CharField(required=True, label='确认密码', write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'nickname', 'phone', 'email', 'password', 'password2']
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError('两次输入的密码不一致')
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)
