from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
import datetime
import random

# 引入当前模块的模型和序列化器
from .models import Role, Menu, DictType, DictData
from .serializers import RoleSerializer, MenuSerializer, DictTypeSerializer, DictDataSerializer

# 引入其他模块的模型用于 Dashboard 统计
from users.models import User
from courses.models import Course, AssignmentSubmission
from competitions.models import Competition, Enrollment, Problem


class RoleViewSet(viewsets.ModelViewSet):
    """
    角色管理接口
    """
    queryset = Role.objects.all().order_by('-created_at')
    serializer_class = RoleSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'key']


class MenuViewSet(viewsets.ModelViewSet):
    """
    菜单管理接口
    """
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    def get_queryset(self):
        # 如果是列表请求，只返回一级菜单（前端通常递归处理）
        # 但为了简单，这里也可以返回所有，由前端构建树
        if self.action == 'list':
            return Menu.objects.filter(parent__isnull=True).order_by('order_num')
        else:
            return Menu.objects.all().order_by('order_num')


class DictTypeViewSet(viewsets.ModelViewSet):
    """
    字典类型接口 (例如: 课程分类, 竞赛类型)
    """
    queryset = DictType.objects.all().order_by('-created_at')
    serializer_class = DictTypeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'type']
    search_fields = ['name', 'type']


class DictDataViewSet(viewsets.ModelViewSet):
    """
    字典数据接口
    """
    queryset = DictData.objects.all().order_by('sort')
    serializer_class = DictDataSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # 🟢 [核心修改] 增加 'dict_type__type'，允许通过 ?dict_type__type=competition_type 查询
    filterset_fields = ['dict_type', 'dict_type__type', 'is_default']
    search_fields = ['label', 'value']


class DashboardViewSet(viewsets.ViewSet):
    """
    首页数据可视化驾驶舱接口
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        # 1. 顶部卡片数据
        user_count = User.objects.count()
        course_count = Course.objects.count()
        competition_count = Competition.objects.count()
        problem_count = Problem.objects.count()

        # 2. 饼图：作业成绩分布
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

        pie_data = [{"name": k, "value": v} for k, v in grade_dist.items()]
        # 防止空数据导致图表难看
        if not submissions.exists():
            pie_data = [{"name": "暂无数据", "value": 0}]

        # 3. 柱状图：近期竞赛报名人数
        recent_comps = Competition.objects.order_by('-start_time')[:5]
        bar_categories = []
        bar_values = []
        for comp in recent_comps:
            count = Enrollment.objects.filter(competition=comp).count()
            bar_categories.append(comp.title)
            bar_values.append(count)

        # 4. 折线图：近7天活跃趋势 (模拟数据，因为没有记录详细日活)
        dates = [(timezone.now() - datetime.timedelta(days=i)).strftime('%m-%d') for i in range(6, -1, -1)]
        # 实际项目中应查询 UserLoginLog 或类似表
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
            "barChart": {"categories": bar_categories, "values": bar_values},
            "lineChart": line_data
        })