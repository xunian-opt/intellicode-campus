from django.db import models
from django.conf import settings


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="课程名称")
    teacher = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                limit_choices_to={'role': 2}, verbose_name="授课教师")
    category = models.CharField(max_length=50, verbose_name="课程分类")
    cover_img = models.ImageField(upload_to='courses/', null=True, blank=True, verbose_name="封面图")
    description = models.TextField(verbose_name="课程简介")
    # 🟢 [新增] 课程大纲
    outline = models.TextField(null=True, blank=True, verbose_name="课程大纲")

    view_count = models.IntegerField(default=0, verbose_name="浏览量")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        db_table = 'tb_course'
        verbose_name = "课程"
        verbose_name_plural = "课程列表"

    def __str__(self):
        return self.title

# 🟢 [新增] 课程资源模型 (视频、PPT、PDF)
class CourseResource(models.Model):
    TYPE_CHOICES = (
        (1, '视频'),
        (2, '课件(PPT/PDF)'),
        (3, '其他资料')
    )
    course = models.ForeignKey(Course, related_name='resources', on_delete=models.CASCADE, verbose_name="所属课程")
    name = models.CharField(max_length=100, verbose_name="资源名称")
    file = models.FileField(upload_to='course_resources/', verbose_name="文件")
    resource_type = models.IntegerField(choices=TYPE_CHOICES, default=2, verbose_name="资源类型")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="上传时间")

    class Meta:
        db_table = 'tb_course_resource'
        verbose_name = "课程资源"
        verbose_name_plural = "课程资源"

class Assignment(models.Model):
    course = models.ForeignKey(Course, related_name='assignments', on_delete=models.CASCADE, verbose_name="所属课程")
    title = models.CharField(max_length=100, verbose_name="作业标题")
    content = models.TextField(verbose_name="作业要求")
    deadline = models.DateTimeField(verbose_name="截止时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="发布时间")

    class Meta:
        db_table = 'tb_assignment'
        verbose_name = "作业发布"
        verbose_name_plural = "作业发布管理"

    def __str__(self):
        return self.title


class AssignmentSubmission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE, verbose_name="对应作业")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="提交学生")
    file = models.FileField(upload_to='assignments/', null=True, blank=True, verbose_name="作业附件")
    content = models.TextField(null=True, blank=True, verbose_name="文本内容")

    score = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="得分")
    is_graded = models.BooleanField(default=False, verbose_name="是否已批改")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        db_table = 'tb_assignment_submission'
        verbose_name = "作业提交"
        verbose_name_plural = "学生作业批改"