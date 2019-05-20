from django.db import models


class Publisher(models.Model):
    categories = (
        (1, "学院"),
        (2, "工作室"),
        (3, "小组")
    )
    name = models.CharField(max_length=30, verbose_name="机构名称")
    category = models.IntegerField(choices=categories, verbose_name="机构类别")  # 代号
    email = models.EmailField(max_length=30, verbose_name="联系邮箱")
    phone = models.CharField(max_length=15, verbose_name="联系电话")  # 可以存座机
    intro = models.TextField(verbose_name="机构简介")
    image = models.ImageField(upload_to="Publisher/%Y/%m", default="Publisher/default.png", 
                              max_length=50, verbose_name="封面图")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    course_num = models.IntegerField(default=0, verbose_name="课程数")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="入驻时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="更新时间")

    class Meta:
        db_table = "publisher"
        verbose_name = "机构"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        return "{}".format(self.name)


class Teacher(models.Model):
    teacher_titles = (
        (1, "讲师"),
        (2, "副教授"),
        (3, "教授"),
        (4, "学生")
    )
    name = models.CharField(max_length=10, verbose_name="教师名称")
    intro = models.CharField(max_length=100, verbose_name="简介")
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="所属机构")
    course_num = models.IntegerField(default=0, verbose_name="课程数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    title = models.IntegerField(choices=teacher_titles, verbose_name="教师职称")
    contact = models.CharField(max_length=30, verbose_name="联系方式", default="暂未透露")
    create_time = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to="teacher/%Y/%m", default="teacher/default.png",
                               verbose_name="教师头像")
    
    class Meta:
        verbose_name = "教师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{}({})".format(self.name, self.title)


