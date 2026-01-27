# backend/init_menus.py
from system.models import Menu
from django.utils import timezone
from django.db import transaction

# 定义所有菜单数据 (严格对应提供的 SQL 脚本)
menus = [
    # ============================================================
    # 1. 系统管理
    # ============================================================
    {
        'id': 1,
        'parent_id': None,
        'title': '系统管理',
        'path': '/system',
        'component': 'Layout',
        'menu_type': 'M',
        'icon': 'el-icon-setting',
        'order_num': 100,
        'perms': None
    },
    {
        'id': 2,
        'parent_id': 1,
        'title': '角色管理',
        'path': 'role',
        'component': 'admin/system/RoleList',
        'menu_type': 'C',
        'icon': 'el-icon-user',
        'order_num': 1,
        'perms': 'system:role:list'
    },
    {
        'id': 3,
        'parent_id': 1,
        'title': '菜单管理',
        'path': 'menu',
        'component': 'admin/system/MenuList',
        'menu_type': 'C',
        'icon': 'el-icon-menu',
        'order_num': 2,
        'perms': 'system:menu:list'
    },
    {
        'id': 4,
        'parent_id': 1,
        'title': '字典管理',
        'path': 'dict',
        'component': 'admin/system/DictTypeList',
        'menu_type': 'C',
        'icon': 'el-icon-notebook-2',
        'order_num': 3,
        'perms': 'system:dict:list'
    },

    # ============================================================
    # 2. 竞赛与题库
    # ============================================================
    {
        'id': 10,
        'parent_id': None,
        'title': '竞赛与题库',
        'path': '/competitions',
        'component': 'Layout',
        'menu_type': 'M',
        'icon': 'el-icon-trophy',
        'order_num': 200,
        'perms': None
    },
    {
        'id': 11,
        'parent_id': 10,
        'title': '题库管理',
        'path': 'problem',
        'component': 'competitions/ProblemList',
        'menu_type': 'C',
        'icon': 'el-icon-cpu',
        'order_num': 1,
        'perms': 'competitions:problem:list'
    },
    {
        'id': 12,
        'parent_id': 10,
        'title': '竞赛活动',
        'path': 'list',
        'component': 'competitions/CompetitionList',
        'menu_type': 'C',
        'icon': 'el-icon-data-analysis',
        'order_num': 2,
        'perms': 'competitions:competition:list'
    },
    {
        'id': 15,
        'parent_id': 10,
        'title': '报名审核',
        'path': 'enrollment',
        'component': 'competitions/EnrollmentList',
        'menu_type': 'C',
        'icon': 'el-icon-s-check',
        'order_num': 3,
        'perms': 'competitions:enrollment:list'
    },

    # ============================================================
    # 3. 考评与成绩管理
    # ============================================================
    {
        'id': 20,
        'parent_id': None,
        'title': '考评与成绩管理',
        'path': '/assessment',
        'component': 'Layout',
        'menu_type': 'M',
        'icon': 'el-icon-s-marketing',
        'order_num': 300,
        'perms': None
    },
    {
        'id': 13,
        'parent_id': 20,
        'title': '评测记录',
        'path': 'records',
        'component': 'competitions/JudgeRecordList',
        'menu_type': 'C',
        'icon': 'el-icon-s-data',
        'order_num': 1,
        'perms': 'competitions:judgerecord:list'
    },
    {
        'id': 14,
        'parent_id': 20,
        'title': '我的错题本',
        'path': 'wrong-book',
        'component': 'competitions/WrongQuestionBook',
        'menu_type': 'C',
        'icon': 'el-icon-notebook-1',
        'order_num': 2,
        'perms': 'competitions:wrongbook:list'
    },
]

try:
    with transaction.atomic():
        print("开始初始化菜单数据...")
        for item in menus:
            # 提取id用于查找或创建
            menu_id = item.pop('id')

            # 使用 update_or_create 确保数据一致性
            # 注意：defaults 包含所有其他字段，如果记录存在则更新这些字段
            menu, created = Menu.objects.update_or_create(
                id=menu_id,
                defaults={
                    **item,
                    'created_at': timezone.now()  # 强制更新时间
                }
            )

            action = "创建" if created else "更新"
            print(f"{action}菜单: [{menu_id}] {item['title']} (Path: {item.get('path')})")

    print("✅ 菜单数据初始化完成！")

except Exception as e:
    print(f"❌ 发生错误: {e}")