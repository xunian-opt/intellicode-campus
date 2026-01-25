from rest_framework import serializers
from .models import Notice, AIChatHistory

class NoticeSerializer(serializers.ModelSerializer):
    author_name = serializers.CharField(source='author.nickname', read_only=True)

    class Meta:
        model = Notice
        fields = '__all__'

class AIChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = AIChatHistory
        fields = '__all__'