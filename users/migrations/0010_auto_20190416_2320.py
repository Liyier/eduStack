# Generated by Django 2.0 on 2019-04-16 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190416_2315'),
    ]

    operations = [
        migrations.AlterField(
            model_name='seesion',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='image/default/1.png', upload_to='image/%Y/%m', verbose_name='头像'),
        ),
    ]
