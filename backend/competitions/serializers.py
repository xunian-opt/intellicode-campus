from rest_framework import serializers
from .models import Problem, Competition, JudgeRecord, Enrollment

class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Problem
        fields = '__all__'

class CompetitionSerializer(serializers.ModelSerializer):
    problems = ProblemSerializer(many=True, read_only=True)
    class Meta:
        model = Competition
        fields = '__all__'

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