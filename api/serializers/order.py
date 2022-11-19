from rest_framework import serializers

from api.models import OrderRequest, OrderRequestDetail, OrderStatus
from api.serializers.item import SimpleItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    item = SimpleItemSerializer()

    class Meta:
        model = OrderRequestDetail
        fields = ["order_request", "item", "quantity"]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ["order", "status", "created_by", "created_at"]


class InputOrderSerializer(serializers.Serializer):
    pass
