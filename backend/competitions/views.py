from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Problem, Competition, JudgeRecord, Enrollment, WrongQuestionBook, ChoiceProblem, ExamPaper
from .serializers import ProblemSerializer, CompetitionSerializer, JudgeRecordSerializer, EnrollmentSerializer, ChoiceProblemSerializer, ExamPaperSerializer


class ChoiceProblemViewSet(viewsets.ModelViewSet):
    queryset = ChoiceProblem.objects.all()
    serializer_class = ChoiceProblemSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['difficulty']
    search_fields = ['title']

class ExamPaperViewSet(viewsets.ModelViewSet):
    queryset = ExamPaper.objects.all().order_by('-created_at')
    serializer_class = ExamPaperSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title']

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class ProblemViewSet(viewsets.ModelViewSet):
    queryset = Problem.objects.all()
    serializer_class = ProblemSerializer
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
    """
    评测记录/成绩管理接口：查询所有提交记录
    API URL: /api/judge_records/
    """
    queryset = JudgeRecord.objects.all().order_by('-submit_time')
    serializer_class = JudgeRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['result', 'competition', 'student', 'problem']
    search_fields = ['student__nickname', 'problem__title']

# [新增] 错题本视图集
class WrongQuestionBookViewSet(viewsets.ReadOnlyModelViewSet):
    """
    错题本管理接口：只返回非AC（错误）的记录
    API URL: /api/wrong_books/
    对应前端页面: /assessment/wrong-book
    """
    # 核心逻辑：自动过滤掉 result='AC' 的记录
    queryset = WrongQuestionBook.objects.exclude(result='AC').order_by('-submit_time')
    serializer_class = JudgeRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['result', 'competition', 'student', 'problem']
    search_fields = ['student__nickname', 'problem__title']