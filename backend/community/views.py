from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Notice, AIChatHistory, Banner
from .serializers import NoticeSerializer, AIChatHistorySerializer, BannerSerializer

class NoticeViewSet(viewsets.ModelViewSet):
    queryset = Notice.objects.all().order_by('-is_top', '-created_at')
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


#轮播图视图
class BannerViewSet(viewsets.ModelViewSet):
    """
    轮播图管理接口
    前端调用: /api/banners/
    """
    # 只显示启用的轮播图，并按 order 排序
    queryset = Banner.objects.filter(is_active=True).order_by('order', '-id')
    serializer_class = BannerSerializer
    # 允许任何人读取(如果是公开首页)，或者仅登录用户读取
    # 这里继承全局配置(通常是IsAuthenticated)，即登录后可见