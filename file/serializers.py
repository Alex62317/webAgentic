from rest_framework import serializers
from .models import FileInfo

class FileInfoSerializer(serializers.ModelSerializer):
    """
    文件信息序列化器
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    file_url = serializers.SerializerMethodField()
    
    def get_file_url(self, obj):
        from django.conf import settings
        from django.urls import reverse
        request = self.context.get('request')
        if request:
            return request.build_absolute_uri(f'/media/{obj.file_path}')
        return f'{settings.MEDIA_URL}{obj.file_path}'
    
    class Meta:
        model = FileInfo
        fields = ['id', 'user_id', 'filename', 'file_path', 'file_url', 'file_size', 'file_type', 'category', 'create_time']
