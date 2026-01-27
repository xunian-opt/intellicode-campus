from django.contrib import admin
from .models import Problem, Competition, JudgeRecord, WrongQuestionBook, Enrollment


@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'time_limit')
    list_filter = ('difficulty',)
    search_fields = ('title',)


@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'start_time', 'end_time', 'created_at')
    filter_horizontal = ('problems',)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'competition', 'status', 'created_at')
    list_filter = ('status', 'competition')


@admin.register(JudgeRecord)
class JudgeRecordAdmin(admin.ModelAdmin):
    """评测记录/成绩管理：显示所有"""
    list_display = ('student', 'problem', 'result', 'score', 'submit_time')
    list_filter = ('result', 'competition')
    search_fields = ('student__username', 'problem__title')


@admin.register(WrongQuestionBook)
class WrongQuestionBookAdmin(admin.ModelAdmin):
    """错题本管理：仅显示错题"""
    list_display = ('student', 'problem', 'result', 'submit_time')
    list_filter = ('result', 'competition')  # 这里的result过滤器只会显示错误的类型
    search_fields = ('student__username', 'problem__title')

    def get_queryset(self, request):
        # 强制只显示非AC记录
        qs = super().get_queryset(request)
        return qs.exclude(result='AC')

    def has_add_permission(self, request):
        # 错题本通常是自动生成的，不允许手动添加
        return False