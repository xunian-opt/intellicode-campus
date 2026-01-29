from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf import settings  # 🟢 引入 settings
from django.conf.urls.static import static  # 🟢 引入 static

# 引入各个模块的 ViewSet
from system.views import RoleViewSet, MenuViewSet, DictTypeViewSet, DictDataViewSet, DashboardViewSet
from users.views import LoginView, UserViewSet, ClassInfoViewSet
from courses.views import CourseViewSet, AssignmentViewSet, AssignmentSubmissionViewSet, CourseResourceViewSet
from competitions.views import ProblemViewSet, CompetitionViewSet, EnrollmentViewSet, JudgeRecordViewSet,WrongQuestionBookViewSet,ChoiceProblemViewSet,ExamPaperViewSet
from community.views import NoticeViewSet, AIChatHistoryViewSet, BannerViewSet

router = DefaultRouter()

# --- 系统管理 (System) ---
router.register(r'system/role', RoleViewSet)
router.register(r'system/menu', MenuViewSet, basename='menu')
router.register(r'system/dict', DictTypeViewSet)
router.register(r'dict-data', DictDataViewSet)
router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# --- 用户管理 (Users) ---
router.register(r'users', UserViewSet)
router.register(r'classes', ClassInfoViewSet)

# --- 课程中心 (Courses) ---
router.register(r'courses', CourseViewSet, basename='course') # 加 basename 避免覆盖冲突
router.register(r'course_resources', CourseResourceViewSet)
router.register(r'assignments', AssignmentViewSet)
router.register(r'submissions', AssignmentSubmissionViewSet)

# --- 竞赛活动管理 (Competitions) ---
router.register(r'problems', ProblemViewSet)
router.register(r'choice_problems', ChoiceProblemViewSet) # 🟢 [新增] 选择题
router.register(r'exam_papers', ExamPaperViewSet) # 🟢 [新增] 试卷
router.register(r'competitions', CompetitionViewSet)
router.register(r'enrollments', EnrollmentViewSet)
# [关键] 对应前端 /assessment/records (评测记录页面)
router.register(r'judge_records', JudgeRecordViewSet)
# [关键] 对应前端 /assessment/wrong-book (错题本页面)
router.register(r'wrong_books', WrongQuestionBookViewSet)

# --- 社区与互动 (Community) ---
router.register(r'notices', NoticeViewSet) #公告
router.register(r'ai_chats', AIChatHistoryViewSet) #AI
router.register(r'banners', BannerViewSet) #轮播图

urlpatterns = [
    path('admin/', admin.site.urls),
    # 登录接口单独配置
    path('api/login/', LoginView.as_view()),
    # 自动生成的 API 路由挂载到 api/ 下
    path('api/', include(router.urls)),
]

# 🟢 [核心修复] 配置媒体文件服务
# 只有在 DEBUG=True (开发模式) 下生效
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)