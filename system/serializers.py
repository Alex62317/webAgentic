from rest_framework import serializers
from .models import SysConfig

class SysConfigSerializer(serializers.ModelSerializer):
    """
    系统配置序列化器
    """
    class Meta:
        model = SysConfig
        fields = ['id', 'config_key', 'config_value', 'config_name', 'config_type', 'remark', 'create_time', 'update_time']
