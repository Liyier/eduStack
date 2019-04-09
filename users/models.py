from django.db import models
from django.contrib.auth.models import AbstractUser
import random, datetime


# Create your models here.
class User(AbstractUser):
    nickname = models.CharField(max_length=30, verbose_name="昵称")
    email = models.EmailField(max_length=150, verbose_name="邮箱")
    mobile = models.CharField(max_length=11)
    is_active = models.BooleanField(default=True, verbose_name="活跃状态")
    birthday = models.DateField(verbose_name="生日", null=True)  #存储 date()
    sex = models.CharField(max_length=5, choices=(('0', "男"), ("1", "女")), default=random.choice(['0', '1']))
    create_time = models.TimeField(auto_now_add=True, verbose_name="创建时间")  # 存储time.time()
    update_time = models.TimeField(auto_now=True, verbose_name="更新时间")  # 每次save操作自动保存
    avatar = models.ImageField(upload_to="image/%Y/%m",
                               default=u"image/default_{}.png".format(random.choice(range(1, 6))), max_length=100)
    # 学院 一对多

    def __str__(self):
        return "<%s, %s>" % (self.nickname, str(self.email))

    def age(self):
        if not self.birthday:
            today = datetime.date.today()
            return today.year - self.birthday.year
        else:
            return -1  # 未知年龄

    class Meta:
        ordering = ["-create_time"]  # 新建用户在前
        verbose_name = "用户"
        verbose_name_plural = verbose_name
