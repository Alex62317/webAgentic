from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import FileInfo
from .serializers import FileInfoSerializer
import os
import uuid
from django.conf import settings

class FileUploadView(APIView):
    """
    文件上传视图
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        if 'file' not in request.FILES:
            return Response({'error': '缺少文件'}, status=status.HTTP_400_BAD_REQUEST)
        
        file = request.FILES['file']
        category = request.data.get('category', 'other')
        
        # 生成唯一文件名
        file_ext = os.path.splitext(file.name)[1]
        unique_filename = f'{uuid.uuid4()}{file_ext}'
        
        # 保存文件
        file_dir = os.path.join('uploads', category, str(request.user.id))
        os.makedirs(os.path.join(settings.MEDIA_ROOT, file_dir), exist_ok=True)
        file_path = os.path.join(file_dir, unique_filename)
        
        with open(os.path.join(settings.MEDIA_ROOT, file_path), 'wb+') as destination:
            for chunk in file.chunks():
                destination.write(chunk)
        
        # 创建文件记录
        file_info = FileInfo.objects.create(
            user=request.user,
            filename=file.name,
            file_path=file_path,
            file_size=file.size,
            file_type=file.content_type,
            category=category
        )
        
        serializer = FileInfoSerializer(file_info, context={'request': request})
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class FileListView(APIView):
    """
    获取用户的文件列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        category = request.query_params.get('category')
        queryset = FileInfo.objects.filter(user=request.user)
        
        if category:
            queryset = queryset.filter(category=category)
        
        serializer = FileInfoSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

class FileDeleteView(APIView):
    """
    删除文件
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, file_id):
        try:
            file_info = FileInfo.objects.get(id=file_id, user=request.user)
            
            # 删除文件
            file_path = os.path.join(settings.MEDIA_ROOT, file_info.file_path)
            if os.path.exists(file_path):
                os.remove(file_path)
            
            file_info.delete()
            return Response({'message': '文件删除成功'}, status=status.HTTP_200_OK)
        except FileInfo.DoesNotExist:
            return Response({'error': '文件不存在'}, status=status.HTTP_404_NOT_FOUND)
