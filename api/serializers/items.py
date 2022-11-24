from rest_framework.serializers import ModelSerializer

from api.models import Item


class FullItemSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    class Meta:
        model = Item
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "brand",
            "img",
            "codename",
            "iva",
            "model",
            "name",
            "price",
            "category_id",
            "created_by",
            "status_id",
        ]


class ItemSerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    class Meta:
        model = Item
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "brand",
            "img",
            "iva",
            "model",
            "name",
            "price",
            "category_id",
            "created_by",
            "codename",
            "is_active",
        ]


class ItemSerializer2(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    class Meta:
        model = Item
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "brand",
            "img",
            "iva",
            "model",
            "name",
            "price",
            "category_id",
            "created_by",
            "is_active",
        ]
