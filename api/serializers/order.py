from rest_framework import serializers

from api.models import OrderRequest, OrderRequestDetail


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = '__all__'


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequestDetail
        fields = ['order_request', 'item', 'quantity']


class InputOrderSerializer(serializers.Serializer):
    pass
