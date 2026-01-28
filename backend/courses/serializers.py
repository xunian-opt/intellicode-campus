from rest_framework import serializers
from .models import Course, Assignment, AssignmentSubmission, CourseResource

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)
    # 嵌套显示资源，方便前端读取
    resources = CourseResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'

# Assignment 和 Submission 序列化器保持不变
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'

class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    student_name = serializers.CharField(source='student.nickname', read_only=True)
    class Meta:
        model = AssignmentSubmission
        fields = '__all__'