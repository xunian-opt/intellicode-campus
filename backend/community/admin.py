from django.contrib import admin
from .models import Notice, AIChatHistory

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'created_at')
    list_filter = ('type',)
    search_fields = ('title', 'content')

@admin.register(AIChatHistory)
class AIChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'user_query', 'created_at')
    search_fields = ('user_query', 'ai_response')