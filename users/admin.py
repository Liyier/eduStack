from django.contrib import admin
from .models import User, EmailVerifyCode, Banner


# Register your models here.
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(EmailVerifyCode)
class EmailVerifyCodeAdmin(admin.ModelAdmin):
    pass


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    pass
