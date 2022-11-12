from rest_framework import serializers

from api.models import Item, OrderRequest, OrderRequestDetail

from .auth import EmployeeSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequestDetail
        fields = ["order_request", "item", "quantity"]


class _Item(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Item
        fields = ("brand", "name", "category")


class _DetailSerializer(serializers.ModelSerializer):
    item = _Item(read_only=True)

    class Meta:
        model = OrderRequestDetail
        fields = ("id", "item", "quantity")


class OrderReadSerializer(serializers.ModelSerializer):
    requested_by = EmployeeSerializer()
    items = _DetailSerializer(read_only=True, many=True)
    warehouse = serializers.CharField(source="warehouse.name")

    class Meta:
        model = OrderRequest
        fields = "__all__"


class InputOrderSerializer(serializers.Serializer):
    pass
