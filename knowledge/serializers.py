from rest_framework import serializers
from .models import KnowledgeInfo, KnowledgeAttach

class KnowledgeInfoSerializer(serializers.ModelSerializer):
    """
    知识库序列化器
    """
    user_id = serializers.ReadOnlyField(source='user.id')
    attach_count = serializers.SerializerMethodField()
    
    def get_attach_count(self, obj):
        return obj.knowledgeattach_set.count()
    
    class Meta:
        model = KnowledgeInfo
        fields = ['id', 'name', 'description', 'user_id', 'attach_count', 'create_time', 'update_time']

class KnowledgeAttachSerializer(serializers.ModelSerializer):
    """
    知识库附件序列化器
    """
    knowledge_id = serializers.ReadOnlyField(source='knowledge.id')
    
    class Meta:
        model = KnowledgeAttach
        fields = ['id', 'knowledge_id', 'filename', 'file_path', 'file_size', 'file_type', 'status', 'create_time', 'update_time']
