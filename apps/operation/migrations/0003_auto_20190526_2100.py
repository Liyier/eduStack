# Generated by Django 2.0 on 2019-05-26 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('operation', '0002_auto_20190518_2117'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usermessage',
            name='user_id',
        ),
        migrations.AddField(
            model_name='usermessage',
            name='from_user_id',
            field=models.IntegerField(default=0, verbose_name='发送消息用户id'),
        ),
        migrations.AddField(
            model_name='usermessage',
            name='to_user_id',
            field=models.IntegerField(default=0, verbose_name='接受消息用户id'),
        ),
    ]