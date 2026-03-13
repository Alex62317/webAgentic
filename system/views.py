from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import SysConfig
from .serializers import SysConfigSerializer

class SysConfigListView(APIView):
    """
    获取系统配置列表
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        config_type = request.query_params.get('config_type')
        queryset = SysConfig.objects.all()
        
        if config_type:
            queryset = queryset.filter(config_type=config_type)
        
        serializer = SysConfigSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SysConfigCreateView(APIView):
    """
    创建系统配置
    """
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = SysConfigSerializer(data=request.data)
        if serializer.is_valid():
            # 检查配置键是否已存在
            config_key = serializer.validated_data['config_key']
            if SysConfig.objects.filter(config_key=config_key).exists():
                return Response({'error': '配置键已存在'}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SysConfigDetailView(APIView):
    """
    获取系统配置详情
    """
    permission_classes = [IsAuthenticated]
    
    def get(self, request, config_id):
        try:
            config = SysConfig.objects.get(id=config_id)
            serializer = SysConfigSerializer(config)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except SysConfig.DoesNotExist:
            return Response({'error': '配置不存在'}, status=status.HTTP_404_NOT_FOUND)

class SysConfigUpdateView(APIView):
    """
    更新系统配置
    """
    permission_classes = [IsAuthenticated]
    
    def put(self, request, config_id):
        try:
            config = SysConfig.objects.get(id=config_id)
            serializer = SysConfigSerializer(config, data=request.data, partial=True)
            if serializer.is_valid():
                # 检查配置键是否与其他配置冲突
                config_key = serializer.validated_data.get('config_key')
                if config_key and config_key != config.config_key:
                    if SysConfig.objects.filter(config_key=config_key).exists():
                        return Response({'error': '配置键已存在'}, status=status.HTTP_400_BAD_REQUEST)
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except SysConfig.DoesNotExist:
            return Response({'error': '配置不存在'}, status=status.HTTP_404_NOT_FOUND)

class SysConfigDeleteView(APIView):
    """
    删除系统配置
    """
    permission_classes = [IsAuthenticated]
    
    def delete(self, request, config_id):
        try:
            config = SysConfig.objects.get(id=config_id)
            config.delete()
            return Response({'message': '配置删除成功'}, status=status.HTTP_200_OK)
        except SysConfig.DoesNotExist:
            return Response({'error': '配置不存在'}, status=status.HTTP_404_NOT_FOUND)
