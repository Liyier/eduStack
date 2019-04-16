from django.db import models
from django.contrib.auth.models import AbstractUser
import random, datetime, time


# Create your models here.
class User(AbstractUser):
    username = models.CharField(max_length=30, verbose_name="用户名", unique=True)
    email = models.EmailField(max_length=150, verbose_name="邮箱")
    mobile = models.CharField(max_length=11, verbose_name="手机号码")
    city = models.CharField(max_length=20, null=True, verbose_name="城市")
    is_active = models.BooleanField(default=True, verbose_name="活跃状态")
    birthday = models.DateField(verbose_name="生日", null=True)  # 存储 date()
    sex = models.CharField(max_length=5, choices=(('0', "男"), ("1", "女")), default=random.choice(['0', '1']),
                           verbose_name="性别")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")  # 存储time.time()
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")  # 每次save操作自动保存
    # 设置五张默认头像
    avatar = models.ImageField(upload_to="image/%Y/%m",
                               default="image/default/{}.png".format(random.choice(range(1, 6))), max_length=100,
                               verbose_name="头像")
    # department = models.ForeignKey

    @property
    def age(self):
        if not self.birthday:
            today = datetime.date.today()
            return today.year - self.birthday.year
        else:
            return -1  # 未知年龄

    def __str__(self):
        return "<%s, %s>" % (self.username, str(self.email))

    class Meta:
        db_table = "user"
        ordering = ["-create_time"]  # 新建用户在前
        verbose_name = "用户"
        verbose_name_plural = verbose_name


class Seesion(models.Model):
    """用于保存当前对话和身份认证"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=100, verbose_name="令牌", null=True, unique=True)
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    def __str__(self):
        if self.token:
            return self.user.username + "\t已登录！"
        else:
            return self.user.username + "\t未登陆！"

    class Meta:
        verbose_name = "会话"
        verbose_name_plural = verbose_name


class Banner(models.Model):
    """首页轮播图, 与其他model很少产生关系"""
    title = models.CharField(max_length=30, verbose_name="标题")
    image = models.ImageField(upload_to="banner/%Y/%m", verbose_name="图片")
    url = models.URLField(max_length=200, verbose_name="图片地址")
    index = models.IntegerField(default=100, verbose_name="图片序号")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "banner"
        verbose_name = "首页轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{}: {}>".format(self.index, self.title)


class EmailVerifyCode(models.Model):
    """邮箱验证码"""
    code = models.CharField(max_length=20, verbose_name="验证码")
    email = models.CharField(max_length=30, verbose_name="邮箱")
    send_time = models.DateTimeField(auto_now_add=True, verbose_name="发送时间")
    send_type = models.CharField(max_length=10, choices=(("register", "注册"), ("forget", "找回密码")), verbose_name="验证码类型")

    class Meta:
        verbose_name = "邮箱验证码"
        verbose_name_plural = verbose_name

    @property
    def is_active(self):
        if time.time() - self.send_time > 60:  # 一分钟过期
            return False
        else:
            return True

    def __str__(self):
        return "<{}  {}: {}>".format(self.send_time, self.email, self.code)
