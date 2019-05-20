from utils.send_mails import send_types_email

import time

from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import User, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, PasswordResetForm


class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            # 支持多种登录方式 Q的语法支持并集(,)，交集(|)
            # 此种登录有有缺陷,用户名与别人的用户名和邮箱不能相等
            user = User.objects.get(Q(username=username) | Q(email=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class LoginView(View):
    def get(self, request):
        return render(request, "login.html", {})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get("username", "")
            password = request.POST.get("password", "")
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user=user)
                    return redirect("/")
                else:
                    return render(request, "login.html", {
                        "msg": "账户未激活请前往注册邮箱点击激活链接",
                        "login_form": login_form
                    })
            else:
                return render(request, "login.html", {
                    "msg": "用户名或密码错误",
                    "login_form": login_form
                })
        else:
            return render(request, "login.html", {"login_form": login_form})


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect("/")


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, "register.html", {"register_form": register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            return render(request, 'register.html', {"register_form": register_form, "msg": "该邮箱已被注册"})
        if register_form.is_valid():
            password = request.POST.get("password")
            new_user = User()
            new_user.username = email
            new_user.email = email
            new_user.password = make_password(password)
            # new_user.save()
            # 为了验证邮箱的真实存在性,所以需要发送激活链接以激活用户
            new_user.is_active = False
            new_user.save()
            send_types_email(email, _type="register")
            return render(request, "login.html", {"register_form": register_form})
        return render(request, 'register.html', {"register_form": register_form})


class ActiveView(View):
    def get(self, request, code):
        """用户激活链接"""
        records = EmailVerifyRecord.objects.filter(code=code)
        if not records:
            return HttpResponse(content="无效的链接！")
        # 基本确定code为唯一的。
        record = records[0]
        if record.send_type == "register" and record.is_active:
            email = record.email
            user = User.objects.get(email=email)
            if user.is_active:
                return HttpResponse(content="用户已激活！")
            else:
                user.is_active = True
                user.save()
                record.is_active = False
                record.save()
                return HttpResponse(content="用户已激活！")
        else:
            return HttpResponse(content="链接已失效！")


class ForgetPasswordView(View):
    """点击忘记密码进入的视图"""

    def get(self, request):
        forget_pwd_form = ForgetPasswordForm()
        return render(request, "forgetpwd.html", {"forget_pwd_form": forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPasswordForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get("email", "")
            if User.objects.filter(email=email).exists():
                send_types_email(
                    email=email,
                    _type="forget"
                )
                return HttpResponse(content="验证用户真实性链接已发送至您的邮箱，请前往点击以完成验证！")
            else:
                msg = "用户不存在！"
                return render(request, "forgetpwd.html", {"forget_pwd_form": forget_pwd_form, "msg": msg})
        else:
            return render(request, "forgetpwd.html", {"forget_pwd_form": forget_pwd_form})


class UserVerifyView(View):
    def get(self, request, code):
        """忘记密码是在用户登出状态修改密码
        所以需要验证用户真实性
        """
        try:
            record = EmailVerifyRecord.objects.get(code=code, is_active=True, send_type="forget")
            if (int(time.time()) - record.send_time.timestamp()) > 60 * 60:
                # 设定过期时间为一个小时
                record.is_active = False
                record.save()
                return HttpResponse(content="链接已过期，请重新申请验证链接！")
            else:
                # 验证通过
                record.is_active = False
                record.save()
                return render(request, "password_reset.html", {"email": record.email})
        except EmailVerifyRecord.DoesNotExist:
            # 无查询记录
            return HttpResponse(content="无效的链接或链接已过期！")


class PasswordResetView(View):
    def get(self, request):
        """get访问直接定位到忘记密码页面"""
        return render(request, "forgetpwd.html", {})
    
    def post(self, request):
        """
        重置密码视图,
        只允许post访问
        """
        password_reset_form = PasswordResetForm(request.POST)
        print(request.POST)
        if password_reset_form.is_valid():
            email = request.POST.get("email", "")
            new_password = request.POST.get("new_password", "")
            sure_password = request.POST.get("sure_password", "")
            
            if new_password == sure_password:
                user = User.objects.get(email=email)
                user.password = make_password(new_password)
                user.save()
                return render(request, "login.html", {"password_reset_form": password_reset_form})
            else:
                msg = "两次密码不一致！"
                return render(request, "password_reset.html", {"password_reset_form": password_reset_form, "msg": msg})
            
        else:
            print("表单错误")
            return render(request, "password_reset.html", {"password_reset_form": password_reset_form})
