from django.db import models


class Course(models.Model):
    level_choices = (
        (1, "初级"),
        (2, "中级"),
        (3, "高级")
    )
    name = models.CharField(max_length=50, verbose_name="课程名称")
    description = models.CharField(max_length=200, verbose_name="描述")
    detail = models.TextField(verbose_name="课程详情")
    level = models.CharField(max_length=5, choices=level_choices, verbose_name="课程难度")
    time = models.IntegerField(default=0, verbose_name="学习时常(分钟数)")
    learn_num = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    image = models.ImageField(upload_to="course/Y%/m%", max_length=50, verbose_name="封面图")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="上线时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    # author

    class Meta:
        db_table = "courses"
        verbose_name = "课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        """以后加上作者"""
        return "<{}>".format(self.name)


class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所属课程")
    name = models.CharField(max_length=50, verbose_name="章节名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{}({})>".format(self.course.name, self.name)


class Video(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, verbose_name="所属章节")
    name = models.CharField(max_length=50, verbose_name="视频名")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        verbose_name = "课程视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{}()>".format(self.name, self.chapter.course.name)


class CourseResource(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="所属课程")
    name = models.CharField(max_length=50, verbose_name="资源名")
    download = models.FileField(upload_to="course_resource/%Y/%m", max_length=100, verbose_name="资源文件")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")

    class Meta:
        db_table = "course_resource"
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "<{}({})>".format(self.name, self.course.name)
