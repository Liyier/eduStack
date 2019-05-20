"""
author@liyi
date: 2019/4/22
"""
import xadmin
from xadmin import views
from .models import *


class CourseCommentsAdmin(object):
    list_display = ["user", "course", "comment", "create_time"]
    search_fields = ["user_name", "course", "comment"]
    list_filter = ["user", "course", "create_time"]


class UserCourseAdmin(object):
    list_display = ["user", "course", "create_time"]
    search_fields = ["user_ name", "course"]
    list_filter = ["user", "course", "create_time"]


class UserFavoriteAdmin(object):
    list_display = ["user", "data_id", "fav_type", "create_time"]
    search_fields = ["user_name", "data_id"]
    list_filter = ["user", "data_id", "fav_type", "create_time"]


class UserMessageAdmin(object):
    list_display = ["user_id", "content", "is_read", "create_time"]
    search_fields = ["user_id", "content"]
    list_filter = ["user_id", "is_read", "create_time"]


xadmin.site.register(CourseComments, CourseCommentsAdmin)
xadmin.site.register(UserCourse, UserCourseAdmin)
xadmin.site.register(UserFavorite, UserFavoriteAdmin)
xadmin.site.register(UserMessage, UserMessageAdmin)
