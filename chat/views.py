from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import ChatModel, ChatSession, ChatMessage
from .serializers import ChatModelSerializer, ChatSessionSerializer, ChatMessageSerializer, ChatRequestSerializer
import openai
from ruoyi_ai.settings import DEFAULT_MODEL_NAME, DEFAULT_MODEL_API_KEY, DEFAULT_MODEL_BASE_URL

# 确保默认模型配置存在
def ensure_default_model():
    """
    确保默认模型配置存在
    """
    if not ChatModel.objects.filter(name=DEFAULT_MODEL_NAME).exists():
        ChatModel.objects.create(
            name=DEFAULT_MODEL_NAME,
            type='ollama',
            api_key=DEFAULT_MODEL_API_KEY,
            base_url=DEFAULT_MODEL_BASE_URL,
            is_active=True
        )

# 初始化默认模型
ensure_default_model()

def chat_index(request):
    """
    聊天界面首页
    """
    return render(request, 'chat/index.html')

class ChatModelListView(APIView):
    """
    获取AI模型列表
    """
    def get(self, request):
        # 确保默认模型存在
        ensure_default_model()
        
        models = ChatModel.objects.filter(is_active=True)
        serializer = ChatModelSerializer(models, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatSessionListView(APIView):
    """
    获取用户的聊天会话列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        sessions = ChatSession.objects.filter(user=request.user)
        serializer = ChatSessionSerializer(sessions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ChatSessionCreateView(APIView):
    """
    创建新的聊天会话
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = ChatSessionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChatSessionDeleteView(APIView):
    """
    删除聊天会话
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            session.delete()
            return Response({'message': '会话删除成功'}, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response({'error': '会话不存在'}, status=status.HTTP_404_NOT_FOUND)

class ChatMessageListView(APIView):
    """
    获取会话的消息列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, session_id):
        try:
            session = ChatSession.objects.get(id=session_id, user=request.user)
            messages = ChatMessage.objects.filter(session=session)
            serializer = ChatMessageSerializer(messages, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ChatSession.DoesNotExist:
            return Response({'error': '会话不存在'}, status=status.HTTP_404_NOT_FOUND)

class ChatSendView(APIView):
    """
    发送聊天消息
    """
    # 移除认证限制，允许未登录用户发送消息
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = ChatRequestSerializer(data=request.data)
        if serializer.is_valid():
            session_id = serializer.validated_data.get('session_id')
            content = serializer.validated_data['content']
            model_name = serializer.validated_data['model_name']
            
            # 确保默认模型存在
            ensure_default_model()
            
            # 获取或创建会话
            if request.user.is_authenticated:
                if session_id:
                    try:
                        session = ChatSession.objects.get(id=session_id, user=request.user)
                    except ChatSession.DoesNotExist:
                        return Response({'error': '会话不存在'}, status=status.HTTP_404_NOT_FOUND)
                else:
                    # 创建新会话
                    session = ChatSession.objects.create(
                        user=request.user,
                        title=content[:50],
                        model_name=model_name
                    )
            else:
                # 未登录用户，不创建会话，直接调用API
                session = None
            
            # 保存用户消息（仅登录用户）
            if request.user.is_authenticated and session:
                user_message = ChatMessage.objects.create(
                    session=session,
                    content=content,
                    role='user',
                    model_name=model_name
                )
            
            # 调用AI模型获取回复
            try:
                # 获取模型配置
                model_config = ChatModel.objects.filter(name=model_name, is_active=True).first()
                if not model_config:
                    # 如果指定模型不存在，使用默认模型
                    model_config = ChatModel.objects.filter(name=DEFAULT_MODEL_NAME, is_active=True).first()
                    if not model_config:
                        return Response({'error': '模型配置不存在'}, status=status.HTTP_404_NOT_FOUND)
                
                # 配置OpenAI客户端
                client = openai.OpenAI(
                    api_key=model_config.api_key,
                    base_url=model_config.base_url
                )
                
                # 构建消息历史
                messages = []
                if request.user.is_authenticated and session:
                    # 获取会话历史
                    history = ChatMessage.objects.filter(session=session).order_by('create_time')
                    for msg in history:
                        messages.append({
                            'role': msg.role,
                            'content': msg.content
                        })
                else:
                    # 未登录用户，只发送当前消息
                    messages.append({
                        'role': 'user',
                        'content': content
                    })
                
                # 调用API获取回复
                response = client.chat.completions.create(
                    model=model_config.name,
                    messages=messages
                )
                
                # 保存助手消息（仅登录用户）
                if request.user.is_authenticated and session:
                    assistant_message = ChatMessage.objects.create(
                        session=session,
                        content=response.choices[0].message.content,
                        role='assistant',
                        model_name=model_name,
                        total_tokens=response.usage.total_tokens
                    )
                else:
                    # 未登录用户，直接返回消息
                    assistant_message = {
                        'content': response.choices[0].message.content,
                        'role': 'assistant',
                        'model_name': model_name
                    }
                
                return Response({
                    'session_id': session.id if session else None,
                    'message': ChatMessageSerializer(assistant_message).data if request.user.is_authenticated and session else assistant_message
                }, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)