"""
author@liyi
date: 2019/5/13
"""
from django import forms


class LoginForm(forms.Form):

    username = forms.CharField(required=True)
    password = forms.CharField(required=True, min_length=5)