from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import CheckList, ListItem, Status


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class ListItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ListItem
        fields = ('id', 'title', 'completed', 'status', 'related_list', 'related_to', 'comments')


class CheckListSerializer(serializers.ModelSerializer):
    class Meta:
        model = CheckList
        fields = ('id', 'name', 'description', 'completed', 'date')
