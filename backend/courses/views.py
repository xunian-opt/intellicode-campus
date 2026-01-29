from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Course, Assignment, AssignmentSubmission, CourseResource
from .serializers import CourseSerializer, AssignmentSerializer, AssignmentSubmissionSerializer, \
    CourseResourceSerializer


class CourseViewSet(viewsets.ModelViewSet):
    # 权限：如果是教师，只能看自己创建的课程；管理员看所有
    serializer_class = CourseSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['category', 'teacher']
    search_fields = ['title', 'teacher__nickname']

    def get_queryset(self):
        user = self.request.user
        # 确保用户已登录
        if not user.is_authenticated:
            return Course.objects.none()

        # 如果是教师(role=2)，只能管理自己的课程；管理员(role=3)管理所有
        # 学生(role=1)也可以查看所有课程
        if getattr(user, 'role', 0) == 2:
            return Course.objects.filter(teacher=user).order_by('-created_at')
        return Course.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        user = self.request.user

        # 🟢 [核心逻辑修复]
        # 使用 getattr 防止 role 字段不存在报错
        user_role = getattr(user, 'role', 0)

        # 1. 如果是教师 (role=2)，强制只能创建自己的课程
        if user_role == 2:
            serializer.save(teacher=user)

        # 2. 如果是管理员 (role=3)
        elif user_role == 3:
            # 检查前端是否传了 'teacher' 字段 (注意：这里检查的是 validated_data)
            # 如果前端传了有效 ID，validated_data 中会有 'teacher' 对象
            if 'teacher' in serializer.validated_data:
                serializer.save()  # 使用前端传的 teacher
            else:
                # 没传则默认给当前管理员
                serializer.save(teacher=user)

        # 3. 其他角色 (兜底)
        else:
            serializer.save(teacher=user)


# 其他 ViewSet 保持不变
class CourseResourceViewSet(viewsets.ModelViewSet):
    queryset = CourseResource.objects.all().order_by('-created_at')
    serializer_class = CourseResourceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['course', 'resource_type']


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