from django.db import models
from users.models import User

class KnowledgeInfo(models.Model):
    """
    知识库信息
    """
    name = models.CharField(max_length=255, verbose_name='知识库名称')
    description = models.TextField(blank=True, verbose_name='知识库描述')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='创建用户')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '知识库'
        verbose_name_plural = '知识库'

class KnowledgeAttach(models.Model):
    """
    知识库附件
    """
    knowledge = models.ForeignKey(KnowledgeInfo, on_delete=models.CASCADE, verbose_name='知识库')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file_path = models.CharField(max_length=512, verbose_name='文件路径')
    file_size = models.IntegerField(verbose_name='文件大小')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    status = models.CharField(max_length=20, verbose_name='处理状态', choices=[('pending', '待处理'), ('processing', '处理中'), ('completed', '已完成'), ('failed', '失败')])
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '知识库附件'
        verbose_name_plural = '知识库附件'
