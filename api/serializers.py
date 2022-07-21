from .models import User
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=100)

    class Meta:
        model = User
        fields = ["username", "password"]
