# Generated by Django 2.0 on 2019-05-19 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='teacher',
            name='avatar',
            field=models.ImageField(default='teacher/default.png', upload_to='teacher/%Y/%m', verbose_name='教师头像'),
        ),
    ]
