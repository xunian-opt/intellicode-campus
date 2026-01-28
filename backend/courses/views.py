from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Assignment, AssignmentSubmission, CourseResource
from .serializers import CourseSerializer, AssignmentSerializer, AssignmentSubmissionSerializer, CourseResourceSerializer

class CourseViewSet(viewsets.ModelViewSet):
    # 权限：如果是教师，只能看自己创建的课程；管理员看所有
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'teacher']
    search_fields = ['title', 'teacher__nickname']

    def get_queryset(self):
        user = self.request.user
        # 如果是教师(role=2)，只能管理自己的课程；管理员(role=3)管理所有
        # 学生(role=1)也可以查看所有课程（前提是有权限配置）
        if user.role == 2:
            return Course.objects.filter(teacher=user).order_by('-created_at')
        return Course.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        # 自动设置创建者
        serializer.save(teacher=self.request.user)

class CourseResourceViewSet(viewsets.ModelViewSet):
    queryset = CourseResource.objects.all().order_by('-created_at')
    serializer_class = CourseResourceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'resource_type']

# AssignmentViewSet 和 AssignmentSubmissionViewSet 保持不变...
class AssignmentViewSet(viewsets.ModelViewSet):
    queryset = Assignment.objects.all().order_by('-created_at')
    serializer_class = AssignmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['course']
    search_fields = ['title', 'course__title']

class AssignmentSubmissionViewSet(viewsets.ModelViewSet):
    queryset = AssignmentSubmission.objects.all().order_by('-submit_time')
    serializer_class = AssignmentSubmissionSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['assignment', 'student', 'is_graded']
    search_fields = ['student__nickname', 'student__username']