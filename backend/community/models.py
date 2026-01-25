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
    type = models.SmallIntegerField(choices=TYPE_CHOICES, default=1, verbose_name="类型")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        db_table = 'tb_notice'
        verbose_name = "系统公告"
        verbose_name_plural = "公告管理"

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