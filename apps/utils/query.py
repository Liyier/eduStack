"""
author@liyi
date: 2019/5/19
"""
from course.models import Course
from publisher.models import Publisher, Teacher
from operation.models import UserFavorite


def get_publisher_courses(publisher_id):
    """
    获取某个发布方下的所有课程
    """
    publisher = Publisher.objects.get(id=publisher_id)
    teachers_id = publisher.teacher_set.all().values("id")
    return Course.objects.filter(teacher_id__in=teachers_id)


def has_fav(user, data_id, fav_type):
    if user.is_authenticated:
        return UserFavorite.objects.filter(user=user, data_id=data_id, fav_type=fav_type).exists()
    else:
        return False
