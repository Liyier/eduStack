from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer
from django.http import JsonResponse
from .models import User
"""
def users(request):
    # function base view 基于函数的视图
    user_list = ["liyi", "cjx"]
    return HttpResponse(json.dumps(user_list))


from django.views import View
from rest_framework.views import APIView  # APIView 继承django原本的view但是多了其他功能
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


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserView(APIView):
    def get(self, request, *args, **kwargs):
        liyi = request.user
        print("liyi is active:", liyi.is_active)
        print("liyi's auth ", request.auth)
        return JsonResponse(data={"msg": "hello world"})
