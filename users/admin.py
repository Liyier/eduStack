from django.contrib import admin
from .models import User, EmailVerifyCode, Banner


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 可以控制在后台admin显示的字段
    pass
