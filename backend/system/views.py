from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Count
from django.utils import timezone
import datetime
import random

from .models import Role, Menu, DictType
from .serializers import RoleSerializer, MenuSerializer, DictTypeSerializer

# 引入其他模块的模型用于统计
from users.models import User
from courses.models import Course, AssignmentSubmission
from competitions.models import Competition, Enrollment, Problem


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all().order_by('-created_at')
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'key']


class MenuViewSet(viewsets.ModelViewSet):
    serializer_class = MenuSerializer
    # 启用过滤，以便支持按标题搜索顶级菜单
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    def get_queryset(self):
        """
        核心修复：
        1. list (获取列表): 只返回 parent 为空的顶级菜单，通过 Serializer 递归显示子菜单。
        2. update/destroy/retrieve (修改/删除/详情): 必须查询所有菜单，否则修改子菜单时会报 404。
        """
        if self.action == 'list':
            return Menu.objects.filter(parent__isnull=True).order_by('order_num')
        else:
            return Menu.objects.all().order_by('order_num')


class DictTypeViewSet(viewsets.ModelViewSet):
    queryset = DictType.objects.all().order_by('-created_at')
    serializer_class = DictTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status']
    search_fields = ['name', 'type']


class DashboardViewSet(viewsets.ViewSet):
    """
    数据可视化驾驶舱接口
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # 1. 顶部卡片：基础数据统计
        user_count = User.objects.count()
        course_count = Course.objects.count()
        competition_count = Competition.objects.count()
        problem_count = Problem.objects.count()

        # 2. 饼图：作业成绩分布 (统计已批改的作业)
        submissions = AssignmentSubmission.objects.filter(is_graded=True, score__isnull=False)
        grade_dist = {'不及格': 0, '及格': 0, '良好': 0, '优秀': 0}

        for sub in submissions:
            s = sub.score
            if s < 60:
                grade_dist['不及格'] += 1
            elif s < 75:
                grade_dist['及格'] += 1
            elif s < 90:
                grade_dist['良好'] += 1
            else:
                grade_dist['优秀'] += 1

        pie_data = [
            {"name": k, "value": v} for k, v in grade_dist.items()
        ]
        if not submissions.exists():
            pie_data = [{"name": "暂无数据", "value": 0}]

        # 3. 柱状图：热门竞赛参与人数 (取最近5场)
        recent_comps = Competition.objects.order_by('-start_time')[:5]
        bar_categories = []
        bar_values = []
        for comp in recent_comps:
            count = Enrollment.objects.filter(competition=comp).count()
            bar_categories.append(comp.title)
            bar_values.append(count)

        # 4. 折线图：近7天数据趋势
        dates = [(timezone.now() - datetime.timedelta(days=i)).strftime('%m-%d') for i in range(6, -1, -1)]

        line_data = {
            "dates": dates,
            "submissions": [random.randint(5, 30) for _ in range(7)],
            "active_users": [random.randint(20, 80) for _ in range(7)]
        }

        return Response({
            "panel": {
                "users": user_count,
                "courses": course_count,
                "competitions": competition_count,
                "problems": problem_count
            },
            "pieChart": pie_data,
            "barChart": {
                "categories": bar_categories,
                "values": bar_values
            },
            "lineChart": line_data
        })