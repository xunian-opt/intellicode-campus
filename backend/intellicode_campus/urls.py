from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 引入各个模块的 ViewSet
from system.views import RoleViewSet, MenuViewSet, DictTypeViewSet, DashboardViewSet
from users.views import LoginView, UserViewSet
from courses.views import CourseViewSet, AssignmentViewSet, AssignmentSubmissionViewSet
from competitions.views import ProblemViewSet, CompetitionViewSet, EnrollmentViewSet, JudgeRecordViewSet
from community.views import NoticeViewSet, AIChatHistoryViewSet

router = DefaultRouter()

# --- 系统管理 (System) ---
router.register(r'system/role', RoleViewSet)

# 🔴 [核心修复] 添加 basename='menu'，因为 MenuViewSet使用了 get_queryset
router.register(r'system/menu', MenuViewSet, basename='menu')

router.register(r'system/dict', DictTypeViewSet)
# 仪表盘接口
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# --- 用户管理 (Users) ---
router.register(r'users', UserViewSet)

# --- 课程中心 (Courses) ---
router.register(r'courses', CourseViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', AssignmentSubmissionViewSet)

# --- 竞赛活动管理 (Competitions) ---
router.register(r'problems', ProblemViewSet)
router.register(r'competitions', CompetitionViewSet)
router.register(r'enrollments', EnrollmentViewSet)
router.register(r'judge_records', JudgeRecordViewSet)

# --- 社区与互动 (Community) ---
router.register(r'notices', NoticeViewSet)
router.register(r'ai_chats', AIChatHistoryViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录接口单独配置
    path('api/login/', LoginView.as_view()),
    # 自动生成的 API 路由挂载到 api/ 下
    path('api/', include(router.urls)),
]