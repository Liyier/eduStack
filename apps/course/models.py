from django.db import models
from publisher.models import Publisher, Teacher


class Course(models.Model):
    
    level_choices = (
        ("初级", "初级"),
        ("中级", "中级"),
        ("高级", "高级")
    )
    name = models.CharField(max_length=50, verbose_name="课程名称")
    # publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, verbose_name="发布方")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="教师")
    description = models.CharField(max_length=200, verbose_name="描述")
    detail = models.TextField(verbose_name="课程详情")
    level = models.CharField(max_length=5, choices=level_choices, verbose_name="课程难度")
    time = models.IntegerField(default=0, verbose_name="学习时长(分钟数)")
    learn_num = models.IntegerField(default=0, verbose_name="学习人数")
    fav_num = models.IntegerField(default=0, verbose_name="收藏人数")
    click_num = models.IntegerField(default=0, verbose_name="点击量")
    image = models.ImageField(upload_to="course/%Y/%m", max_length=50, verbose_name="封面图")
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="上线时间")
    update_time = models.DateTimeField(auto_now=True, verbose_name="修改时间")
    category = models.CharField(max_length=20, default="计算机基础", verbose_name="课程类别")
    notice = models.CharField(max_length=50, default="具备计算机基础知识", verbose_name="课程须知")
    harvest = models.CharField(max_length=50, default="入门计算机编程", verbose_name="课程收获")
    
    class Meta:
        db_table = "courses"
        verbose_name = "课程"
        verbose_name_plural = verbose_name
        
    def __str__(self):
        """以后加上作者"""
        return "<{}-{}>".format(self.name, self.teacher.name)


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
    url = models.URLField(max_length=100, verbose_name="视频链接", null=True)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="添加时间")    
    time = models.IntegerField(default=0, verbose_name="视频长度(秒)")

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
