# Generated by Django 2.0 on 2019-05-19 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('course', '0006_auto_20190519_1654'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('初级', '初级'), ('中级', '中级'), ('高级', '高级')], max_length=5, verbose_name='课程难度'),
        ),
    ]
