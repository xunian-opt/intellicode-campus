from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    # 列表页显示的字段
    list_display = ('username', 'nickname', 'role', 'class_name', 'is_staff', 'date_joined')

    # 侧边栏过滤器
    list_filter = ('role', 'class_name')

    # 搜索框
    search_fields = ('username', 'nickname', 'phone')

    # 编辑页字段分组
    fieldsets = UserAdmin.fieldsets + (
        ('扩展信息', {
            'fields': ('role', 'nickname', 'avatar', 'phone', 'class_name', 'student_id', 'face_feature'),
        }),
    )