# Generated by Django 2.0 on 2019-05-15 18:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='章节名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
            ],
            options={
                'verbose_name': '章节',
                'verbose_name_plural': '章节',
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='课程名称')),
                ('description', models.CharField(max_length=200, verbose_name='描述')),
                ('detail', models.TextField(verbose_name='课程详情')),
                ('level', models.CharField(choices=[(1, '初级'), (2, '中级'), (3, '高级')], max_length=5, verbose_name='课程难度')),
                ('time', models.IntegerField(default=0, verbose_name='学习时常(分钟数)')),
                ('learn_num', models.IntegerField(default=0, verbose_name='学习人数')),
                ('fav_num', models.IntegerField(default=0, verbose_name='收藏人数')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击量')),
                ('image', models.ImageField(max_length=50, upload_to='course/Y%/m%', verbose_name='封面图')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='上线时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='修改时间')),
            ],
            options={
                'verbose_name': '课程',
                'verbose_name_plural': '课程',
                'db_table': 'courses',
            },
        ),
        migrations.CreateModel(
            name='CourseResource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='资源名')),
                ('download', models.FileField(upload_to='course_resource/%Y/%m', verbose_name='资源文件')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='所属课程')),
            ],
            options={
                'verbose_name': '课程资源',
                'verbose_name_plural': '课程资源',
                'db_table': 'course_resource',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='视频名')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='添加时间')),
                ('chapter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Chapter', verbose_name='所属章节')),
            ],
            options={
                'verbose_name': '课程视频',
                'verbose_name_plural': '课程视频',
            },
        ),
        migrations.AddField(
            model_name='chapter',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='course.Course', verbose_name='所属课程'),
        ),
    ]
