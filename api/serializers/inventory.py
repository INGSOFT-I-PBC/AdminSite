from rest_framework.serializers import ModelSerializer

from api.models import Inventory


class FullInventorySerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """
    class Meta: 
        
        model = Inventory
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "quantity",
            "item_id",
            "updated_by_id",
            "warehouse_id",
            "nombreItem",
            "created_at_Item",
            "brandItem",
            "imgItem",
            "ivaItem",
            "modelItem",
            "priceItem",
            "category_id_Item",
            "category_name_Item",
            "status_id_Item",
            "created_by_Item",
            "codename_Item",
            "is_active"
        ]


class InventorySerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    class Meta:
        model = Inventory
        fields = [
            "created_at",
            "updated_at",
            "deleted_at",
            "quantity",
            "item_id",
            "updated_by_id",
            "warehouse_id",
        ]
