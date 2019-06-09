"""
author@liyi
date: 2019/5/23
"""

from django.urls import path
# from django.views.generic import TemplateView
from .views import CoursesView, CourseDetailView, CourseChapterView, CourseCommentsView, VideoPlayView


urlpatterns = [
    path("courses/", view=CoursesView.as_view(), name="courses"),
    path("<int:course_id>/", view=CourseDetailView.as_view(), name="course_detail"),
    path("<int:course_id>/chapters", view=CourseChapterView.as_view(), name="course_chapters"),
    path("<int:course_id>/comments", view=CourseCommentsView.as_view(), name="course_comments"),
    path("video_play/<int:video_id>", view=VideoPlayView.as_view(), name="video_play")
]
