# Generated by Django 2.0 on 2019-05-25 18:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publisher', '0003_teacher_point'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='teacher',
            name='course_num',
        ),
    ]
