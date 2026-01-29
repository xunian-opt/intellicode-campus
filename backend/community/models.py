from django.db import models
from django.conf import settings

class Notice(models.Model):
    """系统公告"""
    TYPE_CHOICES = (
        (1, '普通公告'),
        (2, '竞赛通知'),
        (3, '考试提醒'),
    )
    title = models.CharField(max_length=100, verbose_name="标题")
    content = models.TextField(verbose_name="内容")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="发布人")
    # type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1, verbose_name="类型")
    # 🟢 [修改] 移除 choices 限制，默认值设为字符串 '1' (对应字典键值)
    type = models.CharField(max_length=10, default='1', verbose_name="类型")
    is_top = models.BooleanField(default=False, verbose_name="是否置顶")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        db_table = 'tb_notice'
        verbose_name = "系统公告"
        verbose_name_plural = "公告管理"
        ordering = ['-is_top', '-created_at']

    def __str__(self):
        return self.title

class AIChatHistory(models.Model):
    """AI 智能助教对话记录"""
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="用户")
    user_query = models.TextField(verbose_name="用户提问")
    ai_response = models.TextField(verbose_name="AI回答")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="提问时间")

    class Meta:
        db_table = 'tb_ai_chat'
        verbose_name = "AI咨询记录"
        verbose_name_plural = "AI咨询记录"


class Banner(models.Model):
    """首页轮播图"""
    title = models.CharField(max_length=100, verbose_name="标题")
    image = models.ImageField(upload_to='banners/', verbose_name="图片")
    url = models.CharField(max_length=200, blank=True, null=True, verbose_name="跳转链接")
    order = models.IntegerField(default=0, verbose_name="排序")
    is_active = models.BooleanField(default=True, verbose_name="是否启用")

    class Meta:
        db_table = 'tb_banner'
        ordering = ['order', '-id']
        verbose_name = "轮播图"

class PrivateMessage(models.Model):
    """站内信/师生私信"""
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField(verbose_name="私信内容")
    is_read = models.BooleanField(default=False, verbose_name="已读")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_message'
        ordering = ['-created_at']
        verbose_name = "站内信"