from rest_framework import serializers

from .models import User, Permission


class UserSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass

    username = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "password"]


class PermissionSerializer(serializers.ModelSerializer):
    codename = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=128)

    class Meta:
        model = Permission
        fields = ['codename', 'name']
