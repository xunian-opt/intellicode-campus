from rest_framework import viewsets, filters, status
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

    @action(detail=True, methods=['put'])
    def assign_permissions(self, request, pk=None):
        role = self.get_object()
        menu_ids = request.data.get('menu_ids', [])
        # 设置多对多关系
        role.menus.set(menu_ids)
        return Response({"msg": "权限分配成功"}, status=status.HTTP_200_OK)


class MenuViewSet(viewsets.ModelViewSet):
    """
    菜单管理接口 & 动态路由获取
    """
    serializer_class = MenuSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title']

    # 🟢 强制要求登录，防止匿名访问报错
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # 列表页只返回顶级菜单，避免重复
        if self.action == 'list':
            return Menu.objects.filter(parent__isnull=True).order_by('order_num')
        return Menu.objects.all().order_by('order_num')

    @action(detail=False, methods=['get'])
    def user_routers(self, request):
        """
        获取当前用户的动态路由树 (修复 KeyError 问题)
        """
        user = self.request.user

        # 1. 权限过滤
        if user.is_superuser or user.role == 3:  # 管理员
            menus = Menu.objects.filter(menu_type__in=['M', 'C']).order_by('order_num')
        elif user.system_role:  # 普通用户
            menus = user.system_role.menus.filter(menu_type__in=['M', 'C']).order_by('order_num').distinct()
        else:
            return Response([])

        # 2. 转换为列表字典
        menu_list = list(menus.values(
            'id', 'parent', 'title', 'path', 'component', 'icon', 'menu_type', 'order_num', 'perms'
        ))

        # 3. 构建树形结构
        menu_map = {item['id']: item for item in menu_list}
        roots = []

        # 🟢 [关键修复] 先为所有节点初始化 children，防止后续 sort 报错
        for item in menu_list:
            item['children'] = []

        # 4. 挂载节点
        for item in menu_list:
            parent_id = item['parent']
            # 如果父节点存在且也在权限列表中，则挂载到父节点下
            if parent_id and parent_id in menu_map:
                menu_map[parent_id]['children'].append(item)
            # 只有真正的根节点（无父节点）才放入 roots 列表
            elif not parent_id:
                roots.append(item)

        # 5. 子节点排序 (现在访问 children 是安全的)
        for item in menu_list:
            if item['children']:
                item['children'].sort(key=lambda x: x['order_num'])

        # 根节点排序
        roots.sort(key=lambda x: x['order_num'])

        return Response(roots)


class DictTypeViewSet(viewsets.ModelViewSet):
    """
    字典类型接口
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
    filterset_fields = ['dict_type', 'dict_type__type', 'is_default']
    search_fields = ['label', 'value']


class DashboardViewSet(viewsets.ViewSet):
    """
    首页数据可视化驾驶舱接口
    """
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        user_count = User.objects.count()
        course_count = Course.objects.count()
        competition_count = Competition.objects.count()
        problem_count = Problem.objects.count()

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
        if not submissions.exists():
            pie_data = [{"name": "暂无数据", "value": 0}]

        recent_comps = Competition.objects.order_by('-start_time')[:5]
        bar_categories = []
        bar_values = []
        for comp in recent_comps:
            count = Enrollment.objects.filter(competition=comp).count()
            bar_categories.append(comp.title)
            bar_values.append(count)

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
            "barChart": {"categories": bar_categories, "values": bar_values},
            "lineChart": line_data
        })