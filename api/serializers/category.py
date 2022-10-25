from rest_framework.serializers import ModelSerializer

from api.models import Category


class FullCategorySerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    class Meta:
        model = Category
        fields = [
            "id",
            "created_at",
            "updated_at",
            "description",
            "name",
            "short_name",
            "status_id",
        ]


class CategorySerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    class Meta:
        model = Category
        fields = [
            "created_at",
            "updated_at",
            "description",
            "name",
            "short_name",
            "status_id",
        ]
