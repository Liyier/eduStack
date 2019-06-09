"""
author@liyi
date: 2019/5/25
"""
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class LoginRequiredView(object):
    
    @method_decorator(login_required(login_url='/login/'))
    def dispatch(self, request, *args, **kwargs):
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)