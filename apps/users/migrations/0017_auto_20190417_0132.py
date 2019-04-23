# Generated by Django 2.0 on 2019-04-16 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0016_auto_20190417_0122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailverifycode',
            name='send_time',
            field=models.DateTimeField(auto_now_add=True, verbose_name='发送时间'),
        ),
        migrations.AlterField(
            model_name='emailverifycode',
            name='send_type',
            field=models.CharField(choices=[('register', '注册'), ('forget', '找回密码')], max_length=10, verbose_name='验证码类型'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.CharField(choices=[('0', '男'), ('1', '女')], default='0', max_length=5, verbose_name='性别'),
        ),
    ]