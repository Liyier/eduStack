"""
author@liyi
date: 2019/5/13
"""
from django import forms
from captcha.fields import CaptchaField


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=16)


class RegisterForm(forms.Form):

    email = forms.EmailField(required=True)
    password = forms.CharField(required=True, min_length=8, max_length=16)
    captcha = CaptchaField(error_messages={"invalid": "验证码错误"})
