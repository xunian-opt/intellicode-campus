from django.contrib import admin
from .models import Notice, AIChatHistory, Banner

@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'is_top', 'created_at')
    list_filter = ('type',)
    search_fields = ('title', 'content')
    list_editable = ('is_top',)

@admin.register(AIChatHistory)
class AIChatHistoryAdmin(admin.ModelAdmin):
    list_display = ('student', 'user_query', 'created_at')
    search_fields = ('user_query', 'ai_response')

#新增轮播图
@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'url', 'order', 'is_active')
    list_editable = ('order', 'is_active') # 允许在列表页直接编辑排序和开关