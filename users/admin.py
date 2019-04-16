from django.contrib import admin
from .models import User, EmailVerifyCode, Banner


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # 可以控制在后台admin显示的字段
    list_display = ["username", "sex", "email", "mobile", "birthday", "city", "create_time", "is_staff", "is_superuser"]
    search_fields = ["username", "email", "mobile"]
    list_filter = ["sex", "birthday", "create_time", "city", "is_staff", "is_superuser"]
