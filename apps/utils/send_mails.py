"""
author@liyi
date: 2019/5/15
"""
from edustack import settings
import random

from users.models import EmailVerifyRecord
from django.core.mail import send_mail


def send_register_email(email):
    email_verify_record = EmailVerifyRecord()
    email_verify_record.code = generate_random_string(16)
    email_verify_record.email = email
    email_verify_record.send_type = "register"
    email_verify_record.save()

    email_subject = "eduStack注册激活链接"
    email_body = "请点击下面的连接以激活账号\n{}".format("http://127.0.0.1:8000/user_active/" + email_verify_record.code)

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
    return res
