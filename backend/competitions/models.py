from django.db import models
from django.conf import settings


class Problem(models.Model):
    DIFFICULTY_CHOICES = (('Easy', '简单'), ('Medium', '中等'), ('Hard', '困难'))
    title = models.CharField(max_length=100, verbose_name="题目名称")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='Easy', verbose_name="难度")
    content = models.TextField(verbose_name="题目描述(Markdown)")
    test_cases = models.JSONField(verbose_name="测试用例(JSON)")
    time_limit = models.IntegerField(default=1000, verbose_name="时间限制(ms)")
    memory_limit = models.IntegerField(default=256, verbose_name="内存限制(MB)")

    class Meta:
        db_table = 'tb_problem'
        verbose_name = "题目"
        verbose_name_plural = "编程题库管理"

    def __str__(self): return self.title


class Competition(models.Model):
    title = models.CharField(max_length=100, verbose_name="竞赛名称")
    category = models.CharField(max_length=50, blank=True, null=True, verbose_name="竞赛类型")
    start_time = models.DateTimeField(verbose_name="开始时间")
    end_time = models.DateTimeField(verbose_name="结束时间")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    problems = models.ManyToManyField(Problem, blank=True, related_name='competitions', verbose_name="包含题目")
    description = models.TextField(verbose_name="竞赛规则")

    class Meta:
        db_table = 'tb_competition'
        verbose_name = "竞赛"
        verbose_name_plural = "竞赛活动管理"

    def __str__(self): return self.title


class Enrollment(models.Model):
    STATUS_CHOICES = ((0, '待审核'), (1, '已通过'), (2, '已拒绝'))
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, verbose_name="竞赛")
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="学生")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="状态")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="申请时间")

    class Meta:
        db_table = 'tb_enrollment'
        unique_together = ('competition', 'student')
        verbose_name = "竞赛报名"
        verbose_name_plural = "报名审核管理"


class JudgeRecord(models.Model):
    RESULT_CHOICES = (
        ('Pending', '判题中'), ('AC', '通过'), ('WA', '答案错误'),
        ('TLE', '超时'), ('RE', '运行错误')
    )
    student = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, verbose_name="学生")
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, verbose_name="题目")
    competition = models.ForeignKey(Competition, on_delete=models.SET_NULL, null=True, blank=True,
                                    verbose_name="所属竞赛")
    code = models.TextField(verbose_name="代码")
    result = models.CharField(max_length=20, choices=RESULT_CHOICES, default='Pending', verbose_name="结果")
    score = models.IntegerField(default=0, verbose_name="得分")
    submit_time = models.DateTimeField(auto_now_add=True, verbose_name="提交时间")

    class Meta:
        db_table = 'tb_judge_record'
        verbose_name = "评测记录"
        verbose_name_plural = "评测记录/成绩管理"

    def __str__(self):
        return f"{self.student}-{self.problem}-{self.result}"


# [新增] 错题本代理模型
class WrongQuestionBook(JudgeRecord):
    """
    错题本代理模型：复用 tb_judge_record 表，但用于独立的业务逻辑（只看错题）
    """

    class Meta:
        proxy = True  # 关键：设置为代理模型，不创建新表
        verbose_name = "错题"
        verbose_name_plural = "错题本管理"