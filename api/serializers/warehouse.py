from rest_framework.serializers import (
    CharField,
    DecimalField,
    IntegerField,
    ModelSerializer,
)

from api.models import Inventory, Warehouse, WarehouseTransaction, WhTransactionDetails
from api.models.warehouse import WhTomasFisicas
from api.serializers.common import SimpleStatusSerializer
from api.serializers.item import ItemSerializer, SimpleItemSerializer


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


class WhInventorySerializer(ModelSerializer):

    item = SimpleItemSerializer()
    quantity = IntegerField()

    def to_representation(self, obj):
        """Move fields from item to inventory representation."""
        representation = super().to_representation(obj)
        item_representation = representation.pop("item")
        for key in item_representation:
            representation[key] = item_representation[key]

        return representation

    def to_internal_value(self, data):
        """Move fields related to item to their own item dictionary."""
        item_internal = {}
        for key in ItemSerializer.Meta.fields:
            if key in data:
                item_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal["item"] = item_internal
        return internal

    def update(self, instance, validated_data):
        """Update inventory and item. Assumes there is a item for every inventory."""
        item_data = validated_data.pop("item")
        super().update(instance, validated_data)

        item = instance.item
        for attr, value in item_data.items():
            setattr(item, attr, value)
        item.save()

        return instance

    class Meta:
        model = Inventory
        fields = ["item", "updated_by", "updated_at", "quantity"]


class WhTransactionDetailSerializer(ModelSerializer):
    id = IntegerField()
    item = SimpleItemSerializer()
    quantity = IntegerField()

    def to_representation(self, obj):
        """Move fields from item to Transaction Detail representation."""
        representation = super().to_representation(obj)
        item_representation = representation.pop("item")
        for key in item_representation:
            representation[key] = item_representation[key]

        return representation

    def to_internal_value(self, data):
        """Move fields related to item to their own item dictionary."""
        item_internal = {}
        for key in ItemSerializer.Meta.fields:
            if key in data:
                item_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal["item"] = item_internal
        return internal

    class Meta:
        model = WhTransactionDetails
        fields = ["item", "quantity", "updated_at"]


class WhTransactionSerializer(ModelSerializer):

    id = IntegerField()
    notes = CharField(max_length=300)
    status = SimpleStatusSerializer()

    def to_representation(self, obj):
        """Move fields from status to Transaction representation."""
        representation = super().to_representation(obj)
        status_representation = representation.pop("status")
        representation["status"] = status_representation["name"]

        return representation

    def to_internal_value(self, data):
        """Move fields related to status to their own status dictionary."""
        status_internal = {}
        for key in SimpleStatusSerializer.Meta.fields:
            if key in data:
                status_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal["status"] = status_internal
        return internal

    class Meta:
        model = WarehouseTransaction
        fields = [
            "created_at",
            "created_by",
            "id",
            "notes",
            "status",
            "warehouse_origin",
            "warehouse_destiny",
        ]


class WhTomasFisicasSerializer(ModelSerializer):
    class Meta:
        model = WhTomasFisicas
        fields = "__all__"
