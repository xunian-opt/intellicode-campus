from rest_framework import serializers
from .models import User, ClassInfo


class UserSerializer(serializers.ModelSerializer):
    # 自定义字段：用于前端展示班级名称
    display_class_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'id', 'username', 'password', 'nickname', 'role',
            'avatar', 'phone', 'student_id', 'face_feature',
            'class_info',  # 实际的外键ID (用于修改)
            'display_class_name'  # 展示用的班级名称 (用于列表显示)
        ]
        extra_kwargs = {'password': {'write_only': True}}

    def get_display_class_name(self, obj):
        """
        根据角色智能获取班级名称
        """
        # 情况1：如果是学生 (role=1)，显示他所在的班级
        if obj.role == 1:
            return obj.class_info.name if obj.class_info else "暂无班级"

        # 情况2：如果是教师 (role=2)，显示他管理的所有班级
        elif obj.role == 2:
            # [核心修改] 获取该老师管理的所有班级，并用逗号拼接
            # charge_classes 是 ClassInfo 模型中 teacher 字段定义的 related_name
            my_classes = obj.charge_classes.all()
            if my_classes.exists():
                # 例如返回: "1808班, 1809班"
                return ", ".join([c.name for c in my_classes])
            return "未分配"

        return "-"

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        if 'password' in validated_data:
            password = validated_data.pop('password')
            instance.set_password(password)
        return super().update(instance, validated_data)


class ClassInfoSerializer(serializers.ModelSerializer):
    # 显示班主任的昵称
    teacher_name = serializers.CharField(source='teacher.nickname', read_only=True)
    # 统计班级人数
    student_count = serializers.SerializerMethodField()

    class Meta:
        model = ClassInfo
        fields = ['id', 'name', 'teacher', 'teacher_name', 'student_count', 'created_at']

    def get_student_count(self, obj):
        return obj.students.count()