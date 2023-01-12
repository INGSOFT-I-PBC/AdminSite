from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer, URLField

from api.models import Provider


class ProviderSerializer(ModelSerializer):
    website = URLField()

    class Meta:
        model = Provider
        fields = "__all__"


class PartialProviderSerializer(Serializer):
    """Partial Provider Serializer
    This serializer only would be used to partial data update,
    due all fields are optional (fields that can be modified by a user).

    Args:
        Serializer (rest_framework.serializers.Serializer): The superclass
    """

    id = serializers.IntegerField()
    name = serializers.CharField(max_length=128, required=False)
    document_path = serializers.CharField(max_length=128, required=False)
    bussiness_name = serializers.CharField(max_length=128, required=False)
    address = serializers.CharField(max_length=512, required=False)
    website = serializers.URLField(max_length=100, required=False)
    email = serializers.EmailField(max_length=64, required=False)
    latitude = serializers.DecimalField(
        max_digits=25, decimal_places=17, required=False
    )
    longitude = serializers.DecimalField(
        max_digits=25, decimal_places=17, required=False
    )

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.document_path = validated_data.get(
            "document_path", instance.document_path
        )
        instance.bussiness_name = validated_data.get(
            "bussiness_name", instance.bussiness_name
        )
        instance.website = validated_data.get("website", instance.website)
        instance.email = validated_data.get("email", instance.email)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class SimpleProviderSerializer(ModelSerializer):
    class Meta:
        model = Provider
        fields = ["id", "name"]
