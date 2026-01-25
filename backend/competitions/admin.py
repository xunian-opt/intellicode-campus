from django.contrib import admin
from .models import Problem, Competition, JudgeRecord

@admin.register(Problem)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'time_limit')
    list_filter = ('difficulty',)
    search_fields = ('title',)

@admin.register(Competition)
class CompetitionAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time')
    filter_horizontal = ('problems',)  # 左右选择框

@admin.register(JudgeRecord)
class JudgeRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'problem', 'result', 'score', 'submit_time')
    list_filter = ('result', 'competition')