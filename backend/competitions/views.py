from rest_framework import viewsets, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .models import Problem, Competition, JudgeRecord, Enrollment, WrongQuestionBook, ChoiceProblem, ExamPaper
from .serializers import ProblemSerializer, CompetitionSerializer, JudgeRecordSerializer, EnrollmentSerializer, \
    ChoiceProblemSerializer, ExamPaperSerializer


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

    # 🟢 [新增] 获取“我的竞赛”接口
    @action(detail=False, methods=['get'], permission_classes=[IsAuthenticated])
    def my_competitions(self, request):
        # 查询当前用户已报名的竞赛 (status=1 代表已通过/已报名)
        enrolled_ids = Enrollment.objects.filter(student=request.user, status=1).values_list('competition_id',
                                                                                             flat=True)
        competitions = Competition.objects.filter(id__in=enrolled_ids).order_by('-start_time')

        # 分页处理
        page = self.paginate_queryset(competitions)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(competitions, many=True)
        return Response(serializer.data)


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


class WrongQuestionBookViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = WrongQuestionBook.objects.exclude(result='AC').order_by('-submit_time')
    serializer_class = JudgeRecordSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['result', 'competition', 'student', 'problem']
    search_fields = ['student__nickname', 'problem__title']