# Generated by Django 2.0 on 2019-05-19 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190519_1259'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user/default/default5.jpg', upload_to='user/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], default='1', verbose_name='性别'),
        ),
    ]
