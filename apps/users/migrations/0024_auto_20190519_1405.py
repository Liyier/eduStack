# Generated by Django 2.0 on 2019-05-19 06:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0023_auto_20190519_1404'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='user/default/default4.jpg', upload_to='user/%Y/%m', verbose_name='头像'),
        ),
    ]