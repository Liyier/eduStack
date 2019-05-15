"""edustack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^pgblog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.views.generic import TemplateView
from users.views import LoginView, RegisterView, ActiveView, ForgetPasswordView
import xadmin
from django.urls import path


urlpatterns = [
    url(r'^admin/', xadmin.site.urls),
    url(r'^$', TemplateView.as_view(template_name="index.html"), name="index"),
    url(r'^login/', view=LoginView.as_view(), name="login"),
    url(r"^register/", view=RegisterView.as_view(), name="register"),
    url(r'^captcha/', include('captcha.urls')),
    path("user_active/<code>/", view=ActiveView.as_view()),
    path("forget_pwd/", view=ForgetPasswordView.as_view(), name="forget_password")
]
