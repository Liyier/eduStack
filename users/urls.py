from django.conf.urls import url
from .views import UserViewSet
from rest_framework import routers


router = routers.DefaultRouter()
router.register(r"users", UserViewSet)

urlpatterns = [
]
