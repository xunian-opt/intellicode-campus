from django.db import models


class Role(models.Model):
    """角色管理"""
    name = models.CharField(max_length=50, verbose_name="角色名称")
    key = models.CharField(max_length=50, unique=True, verbose_name="权限字符")
    status = models.BooleanField(default=True, verbose_name="状态")
    remark = models.CharField(max_length=200, null=True, blank=True, verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sys_role'
        verbose_name = "角色"
        verbose_name_plural = "角色管理"


class Menu(models.Model):
    """菜单管理"""
    MENU_TYPE_CHOICES = (
        ('M', '目录'),
        ('C', '菜单'),
        ('F', '按钮'),
    )
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, verbose_name="上级菜单")
    title = models.CharField(max_length=50, verbose_name="菜单名称")
    icon = models.CharField(max_length=50, null=True, blank=True, verbose_name="图标")

    # 路由地址 (仅菜单和目录需要)
    path = models.CharField(max_length=100, null=True, blank=True, verbose_name="路由地址")
    # 组件路径 (仅菜单需要)
    component = models.CharField(max_length=100, null=True, blank=True, verbose_name="组件路径")

    # [新增] 菜单类型
    menu_type = models.CharField(max_length=1, choices=MENU_TYPE_CHOICES, default='C', verbose_name="菜单类型")

    perms = models.CharField(max_length=100, null=True, blank=True, verbose_name="权限标识")
    order_num = models.IntegerField(default=0, verbose_name="排序")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sys_menu'
        verbose_name = "菜单"
        verbose_name_plural = "菜单管理"


class DictType(models.Model):
    """"字典类型 (例如: 课程分类, 竞赛类型)"""
    name = models.CharField(max_length=100, verbose_name="字典名称")
    type = models.CharField(max_length=100, unique=True, verbose_name="字典类型")
    status = models.BooleanField(default=True, verbose_name="状态")
    remark = models.TextField(null=True, blank=True, verbose_name="备注")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'sys_dict_type'
        verbose_name = "字典类型"
        verbose_name_plural = "字典管理"

class DictData(models.Model):
    """字典数据 (例如: 算法课, Python基础)"""
    dict_type = models.ForeignKey(DictType, on_delete=models.CASCADE, related_name='datas')
    label = models.CharField(max_length=100, verbose_name="字典标签")
    value = models.CharField(max_length=100, verbose_name="字典键值")
    sort = models.IntegerField(default=0, verbose_name="排序")
    is_default = models.BooleanField(default=False, verbose_name="是否默认")

    class Meta:
        ordering = ['sort']