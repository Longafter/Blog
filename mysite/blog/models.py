from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericRelation
from django.utils import timezone
from django.urls import reverse

from read_statistics.models import ReadNumMixin, ReadDetail

from ckeditor_uploader.fields import RichTextUploadingField

class BlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name

    class Meta:
        verbose_name = '博客类型'
        verbose_name_plural = verbose_name

class Blog(models.Model, ReadNumMixin):
    title = models.CharField(max_length=50, verbose_name='标题')
    blog_type = models.ForeignKey(BlogType, on_delete=models.CASCADE, verbose_name='博客类型')
    content = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者')
    read_details = GenericRelation(ReadDetail)
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')  # 创建数据时将默认写入当前的时间
    last_updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')  # 每次数据更新时自动写入当前时间

    def get_url(self):
        return reverse('blog_detail', kwargs={'blog_pk': self.pk})

    def get_user(self):
        return self.author

    def get_email(self):
        return self.author.email

    def __str__(self):
        return self.title
        
    class Meta:
        ordering = ['-created_time']
        verbose_name = '博客'
        verbose_name_plural = verbose_name
