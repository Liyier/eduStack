from utils.send_mails import send_register_email

from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import User, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForm, RegisterForm


class UserBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            #支持多种登录方式 Q的语法支持并集(,)，交集(|)
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
                    return render(request, "login.html", {"msg": "账户未激活，请前往注册邮箱点击激活链接"})
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"errors": login_form.errors})


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
            #为了验证邮箱的真实存在性，所以需要发送激活链接以激活用户
            new_user.is_active = False
            new_user.save()
            send_register_email(email)
            return render(request, "login.html", {"register_form": register_form})
        return render(request, 'register.html', {"register_form": register_form})


class ActiveView(View):
    def get(self, request, code):
        """用户激活链接"""
        records = EmailVerifyRecord.objects.filter(code=code)
        if not records:
            return HttpResponse(content="无效的链接")
        for record in records:
            if record.send_type == "register" and record.is_active:
                email = record.email
                user = User.objects.get(email=email)
                if user.is_active:
                    return HttpResponse(content="用户已激活")
                else:
                    user.is_active = True
                    user.save()
                    record.is_active = False
                    record.save()
                    return HttpResponse(content="用户已激活")
            else:
                return HttpResponse(content="链接已失效")


class ForgetPasswordView(View):
    """点击忘记密码进入的视图"""
    def get(self, request):
        return render(request, "forgetpwd.html", {})
