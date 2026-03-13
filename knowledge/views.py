from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import KnowledgeInfo, KnowledgeAttach
from .serializers import KnowledgeInfoSerializer, KnowledgeAttachSerializer
import os
from django.conf import settings

class KnowledgeInfoListView(APIView):
    """
    获取用户的知识库列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        knowledge_list = KnowledgeInfo.objects.filter(user=request.user)
        serializer = KnowledgeInfoSerializer(knowledge_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class KnowledgeInfoCreateView(APIView):
    """
    创建新的知识库
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = KnowledgeInfoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class KnowledgeInfoDetailView(APIView):
    """
    获取知识库详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, knowledge_id):
        try:
            knowledge = KnowledgeInfo.objects.get(id=knowledge_id, user=request.user)
            serializer = KnowledgeInfoSerializer(knowledge)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KnowledgeInfo.DoesNotExist:
            return Response({'error': '知识库不存在'}, status=status.HTTP_404_NOT_FOUND)

class KnowledgeInfoUpdateView(APIView):
    """
    更新知识库信息
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, knowledge_id):
        try:
            knowledge = KnowledgeInfo.objects.get(id=knowledge_id, user=request.user)
            serializer = KnowledgeInfoSerializer(knowledge, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except KnowledgeInfo.DoesNotExist:
            return Response({'error': '知识库不存在'}, status=status.HTTP_404_NOT_FOUND)

class KnowledgeInfoDeleteView(APIView):
    """
    删除知识库
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, knowledge_id):
        try:
            knowledge = KnowledgeInfo.objects.get(id=knowledge_id, user=request.user)
            # 删除相关附件文件
            for attach in knowledge.knowledgeattach_set.all():
                file_path = os.path.join(settings.MEDIA_ROOT, attach.file_path)
                if os.path.exists(file_path):
                    os.remove(file_path)
            knowledge.delete()
            return Response({'message': '知识库删除成功'}, status=status.HTTP_200_OK)
        except KnowledgeInfo.DoesNotExist:
            return Response({'error': '知识库不存在'}, status=status.HTTP_404_NOT_FOUND)

class KnowledgeAttachListView(APIView):
    """
    获取知识库的附件列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, knowledge_id):
        try:
            knowledge = KnowledgeInfo.objects.get(id=knowledge_id, user=request.user)
            attachments = KnowledgeAttach.objects.filter(knowledge=knowledge)
            serializer = KnowledgeAttachSerializer(attachments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except KnowledgeInfo.DoesNotExist:
            return Response({'error': '知识库不存在'}, status=status.HTTP_404_NOT_FOUND)

class KnowledgeAttachUploadView(APIView):
    """
    上传知识库附件
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request, knowledge_id):
        try:
            knowledge = KnowledgeInfo.objects.get(id=knowledge_id, user=request.user)
            if 'file' not in request.FILES:
                return Response({'error': '缺少文件'}, status=status.HTTP_400_BAD_REQUEST)
            
            file = request.FILES['file']
            # 保存文件
            file_dir = os.path.join('knowledge', str(knowledge_id))
            os.makedirs(os.path.join(settings.MEDIA_ROOT, file_dir), exist_ok=True)
            file_path = os.path.join(file_dir, file.name)
            with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            
            # 创建附件记录
            attach = KnowledgeAttach.objects.create(
                knowledge=knowledge,
                filename=file.name,
                file_path=file_path,
                file_size=file.size,
                file_type=file.content_type,
                status='pending'
            )
            
            # 这里可以添加异步处理文件的逻辑，例如文本提取、向量化等
            
            serializer = KnowledgeAttachSerializer(attach)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except KnowledgeInfo.DoesNotExist:
            return Response({'error': '知识库不存在'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class KnowledgeAttachDeleteView(APIView):
    """
    删除知识库附件
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, attach_id):
        try:
            attach = KnowledgeAttach.objects.get(id=attach_id)
            # 验证附件所属的知识库是否属于当前用户
            if attach.knowledge.user != request.user:
                return Response({'error': '无权操作此附件'}, status=status.HTTP_403_FORBIDDEN)
            
            # 删除文件
            file_path = os.path.join(settings.MEDIA_ROOT, attach.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            attach.delete()
            return Response({'message': '附件删除成功'}, status=status.HTTP_200_OK)
        except KnowledgeAttach.DoesNotExist:
            return Response({'error': '附件不存在'}, status=status.HTTP_404_NOT_FOUND)
