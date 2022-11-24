from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, IntegerField, DateTimeField

from api.models import OrderRequest, OrderRequestDetail, OrderStatus
from api.serializers import WarehouseSerializer
from api.serializers.common import EmployeeSerializer, StatusSerializer
from api.serializers.item import SimpleItemSerializer


class OrderSerializer(ModelSerializer):

    id = IntegerField()
    requested_at = DateTimeField()

    class Meta:
        model = OrderRequest
        fields = ["id", "requested_at", "requested_by", "warehouse"]


class FullOrderSerializer(ModelSerializer):

    id = IntegerField()
    requested_at = DateTimeField()
    requested_by = EmployeeSerializer()
    warehouse = WarehouseSerializer()

    class Meta:
        model = OrderRequest
        fields = ["id", "request_at", "request_by", "warehouse"]


class FullOrderStatusSerializer(ModelSerializer):

    id = IntegerField()
    order = OrderSerializer()
    status = StatusSerializer()
    created_by = EmployeeSerializer()
    created_at = DateTimeField()

    class Meta:
        model = OrderStatus
        fields = ["id", "order", "status", "created_by", "created_at"]
        db_table = "order_status"
