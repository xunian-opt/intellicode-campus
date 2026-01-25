from django.contrib import admin
from .models import Role, Menu, DictType

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'key', 'status', 'created_at')
    search_fields = ('name', 'key')
    list_filter = ('status',)

@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('title', 'path', 'perms', 'order_num', 'parent')
    search_fields = ('title', 'perms')
    ordering = ('order_num',)

@admin.register(DictType)
class DictTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'status', 'created_at')
    search_fields = ('name', 'type')