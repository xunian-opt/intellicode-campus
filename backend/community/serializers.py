from rest_framework import serializers
from .models import Notice, AIChatHistory, Banner

class NoticeSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.nickname', read_only=True)
    # 🟢 [新增] 自动获取 choices 的中文显示 (例如: "竞赛通知")
    type_display = serializers.CharField(source='get_type_display', read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'
        read_only_fields = ['author', 'created_at']

class AIChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIChatHistory
        fields = '__all__'

#轮播图序列化
class BannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Banner
        fields = '__all__'