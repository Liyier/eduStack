# Generated by Django 2.0 on 2019-05-19 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='video',
            name='url',
            field=models.URLField(max_length=100, null=True, verbose_name='视频链接'),
        ),
    ]
