from django.db import models

class SysConfig(models.Model):
    """
    系统配置
    """
    config_key = models.CharField(max_length=100, unique=True, verbose_name='配置键')
    config_value = models.TextField(verbose_name='配置值')
    config_name = models.CharField(max_length=255, verbose_name='配置名称')
    config_type = models.CharField(max_length=50, verbose_name='配置类型', choices=[('system', '系统配置'), ('ai', 'AI配置'), ('vector', '向量库配置')])
    remark = models.TextField(blank=True, verbose_name='备注')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '系统配置'
        verbose_name_plural = '系统配置'
