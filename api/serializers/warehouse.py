from rest_framework.serializers import ModelSerializer

from api.models import Warehouse


class FullWarehouseSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    class Meta:
        model = Warehouse
        fields = ['id', 'name', 'latitude', 'longitude', 'status']


class WarehouseSerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """
    class Meta:
        model = Warehouse
        fields = [
            'name',
            'latitude',
            'longitude',
            'status'
        ]
