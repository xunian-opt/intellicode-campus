from rest_framework import viewsets, filters,status
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

# 🟢 [新增] 分配权限接口
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

    def get_queryset(self):
        # 🟢 [核心修复] 列表页只返回顶级菜单 (parent is Null)
        # 因为 Serializer 会自动递归获取子菜单 (children)，如果这里返回所有菜单，
        # 会导致子菜单在前端出现两次（一次在 children 里，一次在根列表中），引发 Duplicate keys 报错。
        if self.action == 'list':
            return Menu.objects.filter(parent__isnull=True).order_by('order_num')

        return Menu.objects.all().order_by('order_num')

    @action(detail=False, methods=['get'])
    def user_routers(self, request):
        """
        获取当前用户的动态路由树
        """
        user = self.request.user

        # 1. 根据角色筛选菜单 (获取所有扁平数据)
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

        # 3. 手动构建纯净的树形结构
        # (避免前端收到 "父节点 + 孤立子节点" 的混合数据)
        menu_map = {item['id']: item for item in menu_list}
        roots = []

        for item in menu_list:
            item['children'] = []
            parent_id = item['parent']

            # 如果父节点存在且也在权限列表中，则挂载到父节点下
            if parent_id and parent_id in menu_map:
                menu_map[parent_id]['children'].append(item)
            # 只有真正的根节点（无父节点）才放入 roots 列表
            elif not parent_id:
                roots.append(item)

        # 4. 子节点排序
        for item in menu_list:
            if item['children']:
                item['children'].sort(key=lambda x: x['order_num'])

        # 根节点排序
        roots.sort(key=lambda x: x['order_num'])

        return Response(roots)


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