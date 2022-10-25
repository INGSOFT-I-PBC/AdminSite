from rest_framework import serializers

from api.models import OrderRequest, OrderRequestDetail, OrderStatus


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequestDetail
        fields = ["order_request", "item", "quantity"]


class OrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatus
        fields = ["order", "status", "created_by", "created_at"]


class InputOrderSerializer(serializers.Serializer):
    pass
