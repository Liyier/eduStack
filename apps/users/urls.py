"""
author@liyi
date: 2019/5/26
"""
from django.urls import path
from .views import UserInfoView, UserCoursesView, UserFavsView, UserMessagesView, AvatarUpdateView
from .views import PasswordModifyView, VerificationCodeView, EmailUpdateView

urlpatterns = [
    path('info/', view=UserInfoView.as_view(), name="user_info"),
    path('courses/', view=UserCoursesView.as_view(), name="user_courses"),
    path('favs/', view=UserFavsView.as_view(), name="user_favs"),
    path('messages/', view=UserMessagesView.as_view(), name="user_messages"),
    path('avatar/', view=AvatarUpdateView.as_view(), name='avatar_update'),
    path('pwd_modify/', view=PasswordModifyView.as_view(), name='password_modify'),
    path('verification_code/', view=VerificationCodeView.as_view(), name="send_verification_code"),
    path('email_update/', view=EmailUpdateView.as_view(), name="email_update")
]