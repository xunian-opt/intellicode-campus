from django.db import models
from django.contrib.auth.models import AbstractUser


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

    class Meta:
        db_table = 'tb_user'
        verbose_name = "用户"
        verbose_name_plural = "用户管理"  # 后台显示的中文菜单名

    def __str__(self):
        return self.nickname or self.username