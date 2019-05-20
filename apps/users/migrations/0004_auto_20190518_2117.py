# Generated by Django 2.0 on 2019-05-18 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20190516_1617'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user/default/4.png', upload_to='user/%Y/%m', verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='user',
            name='sex',
            field=models.IntegerField(choices=[(0, '男'), (1, '女')], default='0', verbose_name='性别'),
        ),
    ]
