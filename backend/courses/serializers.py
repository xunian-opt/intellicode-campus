from rest_framework import serializers
from .models import Course, Assignment, AssignmentSubmission


class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)

    class Meta:
        model = Course
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nickname', read_only=True)

    class Meta:
        model = AssignmentSubmission
        fields = '__all__'