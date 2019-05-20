"""
author@liyi
date: 2019/5/17
"""

from django.urls import path
# from django.views.generic import TemplateView
from .views import PublishersView, PublisherIndexView, PublisherCourseView, PublisherDescView, PublisherTeacherView

urlpatterns = [
    path('publishers/', view=PublishersView.as_view(), name="publishers"),
    path("<int:publisher_id>/", view=PublisherIndexView.as_view(), name="publisher-index"),
    path("<int:publisher_id>/courses/", view=PublisherCourseView.as_view(), name="publisher-course"),
    path("<int:publisher_id>/desc/", view=PublisherDescView.as_view(), name="publisher-desc"),
    path("<int:publisher_id>/teachers/", view=PublisherTeacherView.as_view(), name="publisher-teacher")
]