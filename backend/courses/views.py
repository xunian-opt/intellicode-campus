from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Assignment, AssignmentSubmission
from .serializers import CourseSerializer, AssignmentSerializer, AssignmentSubmissionSerializer

class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all().order_by('-created_at')
    serializer_class = CourseSerializer
    # 启用搜索和过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # 精确过滤: 按分类、授课教师ID筛选
    filterset_fields = ['category', 'teacher']
    # 模糊搜索: 按课程标题、教师姓名搜索
    search_fields = ['title', 'teacher__nickname', 'teacher__username']

class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('-created_at')
    serializer_class = AssignmentSerializer
    # 启用搜索和过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # 精确过滤: 按课程ID筛选
    filterset_fields = ['course']
    # 模糊搜索: 按作业标题、课程名称搜索
    search_fields = ['title', 'course__title']

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by('-submit_time')
    serializer_class = AssignmentSubmissionSerializer
    # 启用搜索和过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    # 精确过滤: 按作业ID、学生ID、是否已批改筛选
    filterset_fields = ['assignment', 'student', 'is_graded']
    # 模糊搜索: 按学生昵称、学生账号搜索
    search_fields = ['student__nickname', 'student__username']