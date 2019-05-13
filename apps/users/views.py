from django.views.generic.base import View
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from .models import User
from django.db.models import Q
from .forms import LoginForm


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
                login(request, user=user)
                return render(request, "index.html")
            else:
                return render(request, "login.html", {"msg": "用户名或密码错误"})
        else:
            return render(request, "login.html", {"errors": login_form.errors})
