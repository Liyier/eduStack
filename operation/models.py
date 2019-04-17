from django.db import models
from users.models import User
from course.models import Course


class CourseComments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comment = models.CharField(max_length=200, verbose_name="评论")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="评论时间")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} commented {} at {}>".format(self.user.username, self.course.name, self.create_time)


class UserCourse(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="学习开始时间")
    # speed_time =  学习时长

    class Meta:
        verbose_name = "课程学习"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} learns {} from {}>".format(self.user.username, self.course.name, self.create_time)


class UserFavorite(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="用户")
    data_id = models.IntegerField(default=0, verbose_name="数据id")  # 学院， 课程， 教师的主键id, 默认无收藏
    fav_type = models.IntegerField(
        choices=(
            (1, "课程"),
            (2, "教师"),
            (3, "学院")
        ), default=1, verbose_name="收藏类型"
    )
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="收藏时间")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} marked  {} {} as favorite at {}>".format(self.user.username, self.fav_type, self.data_id, self.create_time)


class UserMessage(models.Model):
    user_id = models.IntegerField(default=0, verbose_name="用户id") # 0 默认给所有用户发送
    content = models.TextField(verbose_name="消息内容")
    is_read = models.BooleanField(default=False, verbose_name="是否已读")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="接收时间")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{} {}>".format(self.user_id, self.content)


