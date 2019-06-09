from utils.send_mails import send_types_email

import time
import json

from django.shortcuts import render_to_response
from pure_pagination import Paginator, PageNotAnInteger
from django.views.generic.base import View
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from .models import User, EmailVerifyRecord
from django.db.models import Q
from .forms import LoginForm, RegisterForm, ForgetPasswordForm, PasswordResetForm, AvatarUpdateForm
from .forms import PasswordModifyForm, UserInfoForm
from utils.auth import LoginRequiredView
from operation.models import UserCourse, UserFavorite, UserMessage
from course.models import Course
from publisher.models import Teacher, Publisher


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
        
        return render(request, "login.html", {
            "referer": request.__dict__["META"].get("HTTP_REFERER", '')
        })

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
        referer = request.__dict__["META"].get("HTTP_REFERER", '')        
        if referer:
            return redirect(referer)
        else:
            return redirect('/')


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
            first_message = UserMessage(from_user_id=0, to_user_id=new_user.id, 
                                        content="欢迎注册eduStack，祝您在本站有所收获。")
            first_message.save()
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
            return render(request, "password_reset.html", {"password_reset_form": password_reset_form})


class UserInfoView(LoginRequiredView, View):
    def get(self, request):
        return render(request, 'usercenter-info.html', {
            "current_page": 'info'
        })

    def post(self, request):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(user_info_form.errors), content_type='application/json')
    
    
class PasswordModifyView(LoginRequiredView, View):
    def post(self, request):
        pwd_form = PasswordModifyForm(request.POST)
        if pwd_form.is_valid():
            pwd1 = request.POST.get("password1", "")
            pwd2 = request.POST.get("password2", "")
            if pwd1 != pwd2:
                return HttpResponse('{"status":"fail","msg":"密码不一致"}', content_type='application/json')
            user = request.user
            user.password = make_password(pwd2)
            user.save()

            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse(json.dumps(pwd_form.errors), content_type='application/json')


class AvatarUpdateView(LoginRequiredView, View):
    """修改用户头像"""
    def post(self, request):
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponse('{"status":"successed"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"failed"}', content_type='application/json')


class EmailUpdateView(LoginRequiredView, View):
    def post(self, request):
        
        email = request.POST.get('email', '')
        code = request.POST.get('code', '')
        try:
            
            record = EmailVerifyRecord.objects.get(email=email, code=code, send_type='update')
            # 30分钟内有效
            if record.is_active and (int(time.time()) - record.send_time.timestamp()) < (30 * 60):
                user = request.user
                user.email = email
                user.save()
                record.is_active = False
                record.save()
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                record.is_active = False
                record.save()
                return HttpResponse('{"status":"fail", "msg":"验证码已过期"}', content_type='application/json')
        except EmailVerifyRecord.DoesNotExist:
            # 无查询记录
            return HttpResponse('{"status":"fail","msg":"验证码错误"}', content_type='application/json')
        

class VerificationCodeView(LoginRequiredView, View):
    """发送邮箱验证码"""
    def get(self, request):
        email = request.GET.get('email', '')
        if User.objects.filter(email=email).exists():
            return HttpResponse('{"status":"fail","msg":"邮箱已经存在"}', content_type='application/json')
        else:
            status = send_types_email(email, _type='update')
            if status:
                return HttpResponse('{"status":"success"}', content_type='application/json')
            else:
                return HttpResponse('{"status":"fail","msg":"发送失败"}', content_type='application/json')


class UserCoursesView(LoginRequiredView, View):
    def get(self, request):
        user_courses = UserCourse.objects.filter(user_id=request.user.id)
        return render(request, 'usercenter-mycourse.html', {
            "current_page": 'course',
            "user_courses": user_courses
        })
    

class UserFavsView(LoginRequiredView, View):
    def get(self, request):
        # 默认收藏类型为机构
        fav_type = int(request.GET.get("fav_type", 3))
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        page_fav_courses = page_fav_teachers = page_fav_publishers = []
        results = UserFavorite.objects.filter(user=request.user, fav_type=fav_type).values('data_id')

        if fav_type == 1:
            # 收藏类型为课程
            fav_courses =[Course.objects.get(id=item['data_id']) for item in results]
            p = Paginator(fav_courses, per_page=2, request=request)
            page_fav_courses = p.page(page)
        elif fav_type == 2:
            fav_teachers = [Teacher.objects.get(id=item['data_id']) for item in results]
            p = Paginator(fav_teachers, per_page=2, request=request)
            page_fav_teachers = p.page(page)
        else:
            fav_publishers = [Publisher.objects.get(id=item['data_id']) for item in results]
            p = Paginator(fav_publishers, per_page=2, request=request)
            page_fav_publishers = p.page(page)
            
        return render(request, 'usercenter-fav-course.html', {
            'fav_type': fav_type,
            "fav_teachers": page_fav_teachers,
            "fav_publishers": page_fav_publishers,
            "fav_courses": page_fav_courses
        })
    
    
class UserMessagesView(LoginRequiredView, View):
    def get(self, request):
        # 用户系统消息, 即系统广播消息或对用户的私信
        messages = UserMessage.objects.filter(
            Q(to_user_id=0) |
            Q(to_user_id=request.user.id), from_user_id=0
        ).order_by('-create_time')
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(messages, per_page=10, request=request)
        page_messages = p.page(page)
        for message in page_messages.object_list:
            message.is_read = True
            message.save()
        return render(request, 'usercenter-message.html', {
            "messages": page_messages
        })


def page_not_found(request, **kwargs):
    response = render_to_response('404.html', {})
    response.status_code = 404 
    return response


def page_error(request):
    response = render_to_response('500.html', {})
    response.status_code = 500
    return response
