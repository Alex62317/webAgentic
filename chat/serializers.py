from rest_framework import serializers
from .models import ChatModel, ChatSession, ChatMessage

class ChatModelSerializer(serializers.ModelSerializer):
    """
    AI模型序列化器
    """
    class Meta:
        model = ChatModel
        fields = ['id', 'name', 'type', 'api_key', 'base_url', 'is_active', 'create_time']

class ChatSessionSerializer(serializers.ModelSerializer):
    """
    聊天会话序列化器
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    
    class Meta:
        model = ChatSession
        fields = ['id', 'user_id', 'title', 'model_name', 'create_time', 'update_time']

class ChatMessageSerializer(serializers.ModelSerializer):
    """
    聊天消息序列化器
    """
    session_id = serializers.ReadOnlyField(source='session.id')
    
    class Meta:
        model = ChatMessage
        fields = ['id', 'session_id', 'content', 'role', 'deduct_cost', 'total_tokens', 'model_name', 'billing_type', 'create_time']

class ChatRequestSerializer(serializers.Serializer):
    """
    聊天请求序列化器
    """
    session_id = serializers.IntegerField(required=False, allow_null=True)
    content = serializers.CharField(required=True)
    model_name = serializers.CharField(required=True)
