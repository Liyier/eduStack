import xadmin
from xadmin import views
from .models import Publisher, Teacher


class TeacherAdmin(object):
    list_display = ["name", "title", "contact", "publisher", "fav_num", "click_num", "create_time"]
    list_filter = ["title", "fav_num", "click_num", "publisher", "create_time"]
    search_fields = ["name", "contact", "click_num", "fav_num"]


class PublisherAdmin(object):
    list_display = ["name", "email", "phone", "course_num", "fav_num", "click_num"]
    search_fields = ["name", "email", "phone", "fav_num", "click_num"]
    list_filter = ["fav_num", "click_num", "course_num"]


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Publisher, PublisherAdmin)