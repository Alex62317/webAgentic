from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    """
    用户模型
    """
    nickname = models.CharField(max_length=50, blank=True, verbose_name='昵称')
    avatar = models.CharField(max_length=255, blank=True, verbose_name='头像')
    phone = models.CharField(max_length=11, blank=True, verbose_name='手机号')
    email = models.EmailField(blank=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=True, verbose_name='是否激活')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
        app_label = 'users'
