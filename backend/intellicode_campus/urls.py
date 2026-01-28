from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# 引入各个模块的 ViewSet
from system.views import RoleViewSet, MenuViewSet, DictTypeViewSet, DictDataViewSet, DashboardViewSet
from users.views import LoginView, UserViewSet, ClassInfoViewSet
from courses.views import CourseViewSet, AssignmentViewSet, AssignmentSubmissionViewSet, CourseResourceViewSet
from competitions.views import ProblemViewSet, CompetitionViewSet, EnrollmentViewSet, JudgeRecordViewSet,WrongQuestionBookViewSet,ChoiceProblemViewSet,ExamPaperViewSet
from community.views import NoticeViewSet, AIChatHistoryViewSet

router = DefaultRouter()

# --- 系统管理 (System) ---
router.register(r'system/role', RoleViewSet)
router.register(r'system/menu', MenuViewSet, basename='menu')
router.register(r'system/dict', DictTypeViewSet)

# 🟢 [关键修复] 只保留这一行，删除原来的 'system/dict/data'
router.register(r'dict-data', DictDataViewSet)

router.register(r'dashboard', DashboardViewSet, basename='dashboard')

# --- 用户管理 (Users) ---
router.register(r'users', UserViewSet)

# 🟢 [关键修复] 只保留这一行，删除原来的 'users/classes'
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
# 前端 Axios 调用: this.$axios.get('judge_records/')
router.register(r'judge_records', JudgeRecordViewSet)
# [关键] 对应前端 /assessment/wrong-book (错题本页面)
# 前端 Axios 调用: this.$axios.get('wrong_books/')
router.register(r'wrong_books', WrongQuestionBookViewSet)

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