from django.db import models
from django.contrib.auth.models import AbstractUser
from system.models import Role


class ClassInfo(models.Model):
    """班级信息"""
    name = models.CharField(max_length=50, verbose_name="班级名称")
    # 班主任 (关联到教师用户)
    teacher = models.ForeignKey('users.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='charge_classes', verbose_name="班主任")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'tb_class'
        verbose_name = "班级管理"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class User(AbstractUser):
    """
    自定义用户模型
    """
    ROLE_CHOICES = (
        (1, '学生'),
        (2, '教师'),
        (3, '管理员'),
    )

    nickname = models.CharField(max_length=50, verbose_name="姓名", blank=True)
    role = models.SmallIntegerField(choices=ROLE_CHOICES, default=1, verbose_name="角色")
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True, verbose_name="头像")
    phone = models.CharField(max_length=11, null=True, blank=True, verbose_name="手机号")

    # 核心创新点
    face_feature = models.TextField(null=True, blank=True, verbose_name="人脸特征值")

    # 学生专属
    class_name = models.CharField(max_length=50, null=True, blank=True, verbose_name="班级")
    student_id = models.CharField(max_length=20, null=True, blank=True, verbose_name="学号")

    class_info = models.ForeignKey(ClassInfo, on_delete=models.SET_NULL, null=True, blank=True, related_name='students',
                                   verbose_name="所属班级")

    # 🟢 [新增] 关联到系统动态角色
    system_role = models.ForeignKey('system.Role', on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="系统角色")

    def save(self, *args, **kwargs):
        # 如果 system_role 为空，根据 role 自动填充
        if not self.system_role:
            try:
                if self.role == 1:  # 学生
                    self.system_role = Role.objects.filter(name='学生').first()
                elif self.role == 2:  # 教师
                    self.system_role = Role.objects.filter(name='教师').first()
                elif self.role == 3:  # 管理员
                    self.system_role = Role.objects.filter(name='管理员').first()
            except Exception:
                pass  # 防止迁移时 Role 表不存在报错

        super().save(*args, **kwargs)


    class Meta:
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = "用户管理"  # 后台显示的中文菜单名

    def __str__(self):
        return self.nickname or self.username