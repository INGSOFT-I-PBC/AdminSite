from rest_framework.serializers import DateTimeField, IntegerField, ModelSerializer

from api.models import OrderRequest, OrderStatus
from api.serializers import WarehouseSerializer
from api.serializers.common import EmployeeSerializer, StatusSerializer


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
        fields = ["id", "requested_at", "requested_by", "warehouse", "comment"]


class FullOrderStatusSerializer(ModelSerializer):

    status = StatusSerializer()

    def to_representation(self, obj):
        """Move fields from status to purchase representation."""
        representation = super().to_representation(obj)
        status_representation = representation.pop("status")

        representation["status"] = status_representation["name"]

        return representation

    class Meta:
        model = OrderStatus
        fields = ["id", "status", "created_by", "created_at"]
