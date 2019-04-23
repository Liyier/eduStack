import xadmin
from xadmin import views
from .models import Academy, Teacher


class TeacherAdmin(object):
    list_display = ["username", "title", "sex", "email", "mobile", "academy", "fav_num", "click_num", "date_joined"]
    list_filter = ["title", "fav_num", "click_num", "academy", "sex", "date_joined"]
    search_fields = ["username", "mobile", "email", "click_num", "fav_num"]


class AcademyAdmin(object):
    list_display = ["name", "email", "phone", "address", "fav_num", "click_num"]
    search_fields = ["name", "email", "phone", "address", "fav_num", "click_num"]
    list_filter = ["fav_num", "click_num"]


xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(Academy, AcademyAdmin)