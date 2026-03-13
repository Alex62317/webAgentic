from django.db import models
from users.models import User

class FileInfo(models.Model):
    """
    文件信息
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='上传用户')
    filename = models.CharField(max_length=255, verbose_name='文件名')
    file_path = models.CharField(max_length=512, verbose_name='文件路径')
    file_size = models.IntegerField(verbose_name='文件大小')
    file_type = models.CharField(max_length=50, verbose_name='文件类型')
    category = models.CharField(max_length=50, verbose_name='文件分类', choices=[('avatar', '头像'), ('document', '文档'), ('image', '图片'), ('other', '其他')])
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')

    class Meta:
        verbose_name = '文件信息'
        verbose_name_plural = '文件信息'
