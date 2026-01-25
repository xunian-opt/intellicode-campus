from django.contrib import admin
from .models import Course, Assignment, AssignmentSubmission

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'teacher', 'category', 'view_count', 'created_at')
    list_filter = ('category',)
    search_fields = ('title',)

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'deadline', 'created_at')
    list_filter = ('course',)

@admin.register(AssignmentSubmission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('student', 'assignment', 'is_graded', 'score', 'submit_time')
    list_filter = ('is_graded', 'assignment__course')