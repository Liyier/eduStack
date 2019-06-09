"""
author@liyi
date: 2019/5/19
"""
from course.models import Course
from publisher.models import Publisher
from operation.models import UserFavorite
from operation.models import UserCourse


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
    

def get_relate_courses(course):
    user_ids = UserCourse.objects.filter(course=course).values('user_id')
    course_ids = UserCourse.objects.filter(user_id__in=user_ids).values('course_id')
    relate_courses = Course.objects.filter(id__in=course_ids).exclude(id=course.id)
    return relate_courses[:3]

