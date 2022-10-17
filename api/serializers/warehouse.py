from django.forms import DateTimeField
from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, DecimalField, IntegerField

from api.models import Warehouse, Inventory
from api.serializers.item import SimpleItemSerializer
from .common import StatusSerializer


class FullWarehouseSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    id = IntegerField()
    name = CharField(max_length=128, required=False)
    latitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )
    longitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )

    def create(self, validated_data):
        return Warehouse(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Warehouse
        fields = ["id", "name", "latitude", "longitude", "status"]
        extra_kwargs = {"status": {"required": False}}


class WarehouseSerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    name = CharField(max_length=128, required=False)
    latitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )
    longitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )

    def create(self, validated_data):
        return Warehouse(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.latitude = validated_data.get("latitude", instance.latitude)
        instance.longitude = validated_data.get("longitude", instance.longitude)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance

    class Meta:
        model = Warehouse
        fields = ["name", "latitude", "longitude"]
        extra_kwargs = {"status": {"required": False}}


class InventorySerializer(ModelSerializer):

    item = SimpleItemSerializer()
    quantity = IntegerField()

    class Meta:
        model = Inventory
        fields = ["item", "quantity", "updated_by"]
