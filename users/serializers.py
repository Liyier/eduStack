from django.contrib.auth.models import Group
from rest_framework import serializers
from rest_framework.views import APIView  # APIView 继承django原本的view但是多了其他功能
from .models import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class UserView(APIView):
    def get(self):
        self.dispatch()
