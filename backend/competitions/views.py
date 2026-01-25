from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Problem, Competition, JudgeRecord, Enrollment
from .serializers import ProblemSerializer, CompetitionSerializer, JudgeRecordSerializer, EnrollmentSerializer

class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
    # 搜索与过滤
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['difficulty']
    search_fields = ['title', 'content']

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all().order_by('-start_time')
    serializer_class = CompetitionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'description']

class EnrollmentViewSet(viewsets.ModelViewSet):
    queryset = Enrollment.objects.all().order_by('-created_at')
    serializer_class = EnrollmentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['status', 'competition']
    search_fields = ['student__nickname', 'student__username', 'competition__title']

class JudgeRecordViewSet(viewsets.ModelViewSet):
    queryset = JudgeRecord.objects.all().order_by('-submit_time')
    serializer_class = JudgeRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['result', 'competition', 'student', 'problem']
    search_fields = ['student__nickname', 'problem__title']