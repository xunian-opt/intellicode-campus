from rest_framework import serializers
from .models import Problem, Competition, JudgeRecord, Enrollment, ChoiceProblem, ExamPaper

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'
# 🟢 选择题序列化器
class ChoiceProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChoiceProblem
        fields = '__all__'

class ExamPaperSerializer(serializers.ModelSerializer):
    created_by_name = serializers.CharField(source='created_by.nickname', read_only=True)
    # 简单显示题目数量，详情可以另写接口或复用
    choice_count = serializers.IntegerField(source='choice_problems.count', read_only=True)
    prog_count = serializers.IntegerField(source='programming_problems.count', read_only=True)

    class Meta:
        model = ExamPaper
        fields = '__all__'
# 🟢 [关键修改] 将 created_by 设为只读，跳过前端必填校验
        read_only_fields = ['created_by', 'created_at']

class CompetitionSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    class Meta:
        model = Competition
        fields = ['id', 'title', 'category', 'description', 'start_time', 'end_time', 'created_at', 'problems']

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