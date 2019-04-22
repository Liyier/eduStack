# Generated by Django 2.0 on 2019-04-16 17:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_auto_20190417_0018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banner',
            name='index',
            field=models.IntegerField(default=100, verbose_name='图片序号'),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='image/default/2.png', upload_to='image/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('0', '男'), ('1', '女')], default='1', max_length=5, verbose_name='性别'),
        ),
    ]