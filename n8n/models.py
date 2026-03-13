from django.db import models
from django.conf import settings


class Workflow(models.Model):
    """
    工作流模型
    """
    name = models.CharField(max_length=255, verbose_name='工作流名称')
    description = models.TextField(blank=True, verbose_name='工作流描述')
    definition = models.JSONField(verbose_name='工作流定义')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='创建者')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    
    class Meta:
        verbose_name = '工作流'
        verbose_name_plural = '工作流管理'
    
    def __str__(self):
        return self.name


class Execution(models.Model):
    """
    工作流执行历史模型
    """
    STATUS_CHOICES = (
        ('pending', '等待执行'),
        ('running', '执行中'),
        ('success', '执行成功'),
        ('failed', '执行失败'),
    )
    
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE, verbose_name='关联工作流')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='执行状态')
    input_data = models.JSONField(blank=True, null=True, verbose_name='输入数据')
    output_data = models.JSONField(blank=True, null=True, verbose_name='输出数据')
    error_message = models.TextField(blank=True, verbose_name='错误信息')
    started_at = models.DateTimeField(auto_now_add=True, verbose_name='开始时间')
    completed_at = models.DateTimeField(blank=True, null=True, verbose_name='完成时间')
    
    class Meta:
        verbose_name = '执行历史'
        verbose_name_plural = '执行历史管理'
    
    def __str__(self):
        return f"{self.workflow.name} - {self.status}"
