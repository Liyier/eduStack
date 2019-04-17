from django.db import models
from users.models import User


class Academy(models.Model):
    academy_names = (
        (1001, "计算机与科学学院"),
        (1002, "通信与信息工程学院"),
        (1003, "经济管理学院/现代邮政学院"),
        (1004, "生物信息学院"),
        (1005, "理学院"),
        (1007, "传媒艺术学院"),
        (1008, "外国语学院"),
        (1009, "光电工程学院/重庆国际半导体学院"),
        (1010, "先进制造工程学院"),
        (1011, "自动化学院"),
        (1012, "软件工程学院"),
        (1013, "国际学院"),
        (1014, "网络空间安全与信息法学院"),
        (1015, "马克思学院"),
        (1016, "体育学院"),

    )
    name = models.IntegerField(choices=academy_names, verbose_name="学院名称")  # 学院代号
    email = models.EmailField(max_length=30, verbose_name="联系邮箱")
    phone = models.CharField(max_length=15, verbose_name="联系电话")  # 可以存座机
    address = models.CharField(max_length=50, verbose_name="学院地址")
    intro = models.TextField(verbose_name="学院简介")
    image = models.ImageField(upload_to="academy/%Y/%m", max_length=50, verbose_name="封面图")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "academy"
        verbose_name = "学院"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.name)



class Teacher(User):
    """继承用户 model"""
    teacher_titles = (
        (1, "讲师"),
        (2, "副教授"),
        (3, "教授")
    )
    intro = models.CharField(max_length=100, verbose_name="简介")
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, verbose_name="所属学院")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    title = models.IntegerField(choices=teacher_titles, verbose_name="教师职称")

    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}".format(self.username)


