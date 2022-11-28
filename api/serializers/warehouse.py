from rest_framework.serializers import CharField, ModelSerializer

from api.models.warehouse import Warehouse, WarehouseBarcode


class FullWarehouseSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

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


class ROBarcodeSerializer(ModelSerializer):

    created_by = CharField(source="created_by.name")

    class Meta:
        model = WarehouseBarcode
        fields = "__all__"


class WhBarcodeSerializer(ModelSerializer):
    class Meta:
        model = WarehouseBarcode
        fields = "__all__"
