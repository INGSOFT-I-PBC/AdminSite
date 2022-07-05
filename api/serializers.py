from .models import User, Permission
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'lastname', 'email', 'username', 'password']


class PermissionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Permission
        fields = ['id', 'name']
