from rest_framework import serializers

from .models import User


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
