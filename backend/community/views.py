from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notice, AIChatHistory
from .serializers import NoticeSerializer, AIChatHistorySerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-created_at')
    serializer_class = NoticeSerializer
    # 启用搜索和过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['type'] # 按类型筛选
    search_fields = ['title', 'content'] # 按标题内容搜索

    def perform_create(self, serializer):
        # 自动将当前登录用户设为发布人
        serializer.save(author=self.request.user)

class AIChatHistoryViewSet(viewsets.ModelViewSet):
    queryset = AIChatHistory.objects.all().order_by('-created_at')
    serializer_class = AIChatHistorySerializer
    # 启用搜索和过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['student'] # 按学生筛选
    search_fields = ['student__nickname', 'student__username', 'user_query', 'ai_response'] # 搜索对话内容