import xadmin
from xadmin import views
from .models import Course, Chapter, Video, CourseResource


class CourseAdmin(object):
    list_display = ["name", "level", "description", "time", "fav_num", "learn_num", "click_num", "create_time"]
    search_fields = ["name", "description"] # author or publisher
    list_filter = ["level", "time", "fav_num", "learn_num", "click_num", "create_time"]


class ChapterAdmin(object):
    list_display = ["name", "course", "create_time"]
    search_fields = ["name", "course"]
    list_filter = ["name", "course", "create_time"]


class VideoAdmin(object):
    list_display = ["name", "chapter", "create_time"]
    search_fields = ["name", "chapter"]
    list_filter = ["name", "chapter", "create_time"]


class CourseResourceAdmin(object):
    list_display = ["name", "course", "download", "create_time"]
    search_fields = ["name", "course", "download"]
    list_filter = ["name", "course", "download", "create_time"]


xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)