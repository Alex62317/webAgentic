from django.db import models
from users.models import User

class ChatModel(models.Model):
    """
    AI模型配置
    """
    name = models.CharField(max_length=100, verbose_name='模型名称')
    type = models.CharField(max_length=50, verbose_name='模型类型')
    api_key = models.CharField(max_length=255, verbose_name='API密钥')
    base_url = models.CharField(max_length=255, verbose_name='API基础URL')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = 'AI模型'
        verbose_name_plural = 'AI模型'

class ChatSession(models.Model):
    """
    聊天会话
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户')
    title = models.CharField(max_length=255, verbose_name='会话标题')
    model_name = models.CharField(max_length=100, verbose_name='使用的模型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '聊天会话'
        verbose_name_plural = '聊天会话'

class ChatMessage(models.Model):
    """
    聊天消息
    """
    session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, verbose_name='会话')
    content = models.TextField(verbose_name='消息内容')
    role = models.CharField(max_length=20, verbose_name='角色', choices=[('user', '用户'), ('assistant', '助手')])
    deduct_cost = models.DecimalField(max_digits=10, decimal_places=4, null=True, blank=True, verbose_name='扣除金额')
    total_tokens = models.IntegerField(null=True, blank=True, verbose_name='累计Tokens')
    model_name = models.CharField(max_length=100, verbose_name='模型名称')
    billing_type = models.CharField(max_length=20, null=True, blank=True, verbose_name='计费类型')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '聊天消息'
        verbose_name_plural = '聊天消息'
