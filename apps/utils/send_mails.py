"""
author@liyi
date: 2019/5/15
"""
from edustack import settings
import random
import time

from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def send_types_email(email, _type):
    email_verify_record = EmailVerifyRecord()
    email_verify_record.code = generate_random_string(16)
    email_verify_record.email = email
    if _type == "register":
        email_verify_record.send_type = _type
        email_verify_record.save()
        email_subject = "eduStack注册激活链接"
        email_body = "请点击下面的链接以激活账号\n{}".format("http://127.0.0.1:8000/user_active/" + email_verify_record.code)

    elif _type == "forget":
        email_verify_record.send_type = _type
        email_verify_record.save()
        email_subject = "eduStack修改密码链接"
        email_body = "请点击下面的链接以完成邮箱验证并跳转至重置密码页面\n{}".format("http://127.0.0.1:8000/password_forget/" + email_verify_record.code)
    else:
        # 预防以后还有其他send_type扩展
        return None
    status = send_mail(
        subject=email_subject,
        message=email_body,
        from_email=settings.EMAIL_FROM,
        recipient_list=[email]
    )
    return status


def generate_random_string(length):
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    stop = len(chars) - 1
    res = ""
    for i in range(length):
        res += chars[random.randint(0, stop)]
    # 再加上当前时间的16进制字符串，保证其唯一性
    return res + hex(int(time.time()))
