from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, DecimalField, IntegerField

from api.models import Warehouse


class FullWarehouseSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    id = IntegerField()
    name = CharField(max_length=128)
    latitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )
    longitude = DecimalField(
        max_digits=10, decimal_places=6, required=False, allow_null=True
    )
    status = IntegerField()

    def create(self, validated_data):
        return Warehouse(**validated_data)

    class Meta:
        model = Warehouse
        fields = ["id", "name", "latitude", "longitude", "status"]


class WarehouseSerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    class Meta:
        model = Warehouse
        fields = ["name", "latitude", "longitude", "status"]
