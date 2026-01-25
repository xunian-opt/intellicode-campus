from rest_framework import serializers
from .models import Role, Menu, DictType

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

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
        model = DictType
        fields = '__all__'