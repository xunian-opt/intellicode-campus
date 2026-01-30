from rest_framework import serializers
from .models import Problem, Competition, JudgeRecord, Enrollment, ChoiceProblem, ExamPaper

class ProblemSerializer(serializers.ModelSerializer):
    # 🟢 [新增] 获取当前用户的做题状态 (AC:已通过, Attempted:尝试过, Todo:未开始)
    user_status = serializers.SerializerMethodField()
    # 🟢 [新增] 通过率 (模拟数据，实际需聚合查询)
    acceptance_rate = serializers.SerializerMethodField()

    class Meta:
        model = Problem
        fields = '__all__'

    def get_user_status(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            # 检查是否有 AC 记录
            if JudgeRecord.objects.filter(student=request.user, problem=obj, result='AC').exists():
                return 'AC'
            # 检查是否有提交记录
            elif JudgeRecord.objects.filter(student=request.user, problem=obj).exists():
                return 'Attempted'
        return 'Todo'

    def get_acceptance_rate(self, obj):
        # 简单计算：AC数 / 总提交数 (如果没有提交，返回 0%)
        total = JudgeRecord.objects.filter(problem=obj).count()
        if total == 0: return '0%'
        ac_count = JudgeRecord.objects.filter(problem=obj, result='AC').count()
        return f"{int((ac_count / total) * 100)}%"

class ChoiceProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceProblem
        fields = '__all__'

class ExamPaperSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.nickname', read_only=True)
    choice_count = serializers.IntegerField(source='choice_problems.count', read_only=True)
    prog_count = serializers.IntegerField(source='programming_problems.count', read_only=True)

    class Meta:
        model = ExamPaper
        fields = '__all__'
        read_only_fields = ['created_by', 'created_at']

class CompetitionSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    # 🟢 [新增] 报名状态
    is_enrolled = serializers.SerializerMethodField()

    class Meta:
        model = Competition
        fields = ['id', 'title', 'category','cover_img', 'description', 'start_time', 'end_time', 'created_at', 'problems', 'is_enrolled']

    def get_is_enrolled(self, obj):
        request = self.context.get('request')
        if request and hasattr(request, 'user') and request.user.is_authenticated:
            return Enrollment.objects.filter(student=request.user, competition=obj, status=1).exists()
        return False

class EnrollmentSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nickname', read_only=True)
    competition_title = serializers.CharField(source='competition.title', read_only=True)
    class Meta:
        model = Enrollment
        fields = '__all__'

class JudgeRecordSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nickname', read_only=True)
    problem_title = serializers.CharField(source='problem.title', read_only=True)
    class Meta:
        model = JudgeRecord
        fields = '__all__'