from django.shortcuts import render, HttpResponse
from django.views import View
import json

"""
def users(request):
    # function base view 基于函数的视图
    user_list = ["liyi", "cjx"]
    return HttpResponse(json.dumps(user_list))


class StudentView(View):
    # 必须继承view， django才会为你自动选择方法, 并实现同样的视图函数功能
    # CBV class base view
    def get(self, request, *args, **kwargs):
        return HttpResponse("get")
    
    def post(self, request, *args, **kwargs):
        return HttpResponse("post")
    
# in urls.py
# url(r"^students/", views.StudentView.as_view())
"""