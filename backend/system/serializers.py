from rest_framework import serializers
from .models import Role, Menu, DictType, DictData

class RoleSerializer(serializers.ModelSerializer):
    # 读取时：返回菜单ID列表，方便前端树形控件回显
    menu_ids = serializers.SerializerMethodField()

    class Meta:
        model = Role
        fields = '__all__'

    def get_menu_ids(self, obj):
        return list(obj.menus.values_list('id', flat=True))

class MenuSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Menu
        fields = '__all__'

    def get_children(self, obj):
        # 简单递归获取子菜单 (仅用于展示树形结构)
        if obj.menu_set.exists():
            return MenuSerializer(obj.menu_set.all(), many=True).data
        return []

class DictTypeSerializer(serializers.ModelSerializer):
    class Meta:
        # 🔴 注意：这里必须是 DictType，不能是 DictData
        model = DictType
        fields = '__all__'

class DictDataSerializer(serializers.ModelSerializer):
    class Meta:
        # 🔴 这里才是 DictData
        model = DictData
        fields = '__all__'