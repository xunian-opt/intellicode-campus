from rest_framework import serializers
from .models import Course, Assignment, AssignmentSubmission, CourseResource
from users.models import User # 引入用户模型用于下拉选择

class CourseResourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseResource
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    # 用于显示的字段 (只读)
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)
    resources = CourseResourceSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = '__all__'
        # 🟢 [核心修改] 移除了 'teacher'，允许前端传入 teacher ID
        read_only_fields = ['created_at', 'view_count', 'like_count', 'fav_count']

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