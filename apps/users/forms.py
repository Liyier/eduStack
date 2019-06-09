"""
author@liyi
date: 2019/5/13
"""
from django import forms
from captcha.fields import CaptchaField
from .models import User


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=16)
    # referer = forms.CharField(max_length=60)


class RegisterForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=16)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class ForgetPasswordForm(forms.Form):
    email = forms.EmailField(required=True)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})


class PasswordResetForm(forms.Form):
    email = forms.EmailField(required=True)
    new_password = forms.CharField(required=True, min_length=8, max_length=16)
    sure_password = forms.CharField(required=True, min_length=8, max_length=16)
    
    
class AvatarUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['avatar']


class PasswordModifyForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8, max_length=16)
    password2 = forms.CharField(required=True, min_length=8, max_length=16)
    
    
class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'sex', 'birthday', 'city', 'mobile']

