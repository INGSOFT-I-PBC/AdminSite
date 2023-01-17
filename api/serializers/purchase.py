from django.forms import DateTimeField, IntegerField
from rest_framework import serializers
from rest_framework.fields import CharField

from api.models import Purchase
from api.models.orders import OrderRequest
from api.models.purchases import PurchaseChild, PurchaseDetail, PurchaseStatus
from api.models.warehouse import Warehouse
from api.serializers.common import SimpleStatusSerializer
from api.serializers.inovice import SimpleInvoiceSerializer
from api.serializers.product import SimpleProductSerializer, SimpleVariantSerializer
from api.serializers.provider import SimpleProviderSerializer
from api.serializers.users import EmployeeSerializer


class SimplePurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = ["order_origin", "reference", "warehouse"]


class SimplePurchaseChildSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseChild
        fields = ["purchase_header", "provider", "comment"]


class SimplePurchaseDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseDetail
        fields = "__all__"


class SimplePurchaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseStatus
        fields = ['created_by', "purchase", "status"]


class PurchaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Purchase
        fields = "__all__"


class PurchaseChildSerializer(serializers.ModelSerializer):
    invoice = SimpleInvoiceSerializer()
    provider = SimpleProviderSerializer()

    class Meta:
        model = PurchaseChild
        fields = "__all__"


class PurchaseDetailSerializer(serializers.ModelSerializer):

    product = SimpleProductSerializer()
    variant = SimpleVariantSerializer()

    class Meta:
        model = PurchaseDetail
        fields = "__all__"


class AttachedOrderRequestSerializer(serializers.ModelSerializer):

    revised_by = EmployeeSerializer()

    class Meta:
        model = OrderRequest
        fields = ["id", "comment", "revised_by", "requested_at"]


class AttachedWarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = ["id", "name"]


class PurchaseStatusSerializer(serializers.ModelSerializer):
    """
    Simple purchase serializers to get minimum information of a purchase with
    the provider reference and last status registered.
    """

    status = CharField()
    order_origin = AttachedOrderRequestSerializer()
    warehouse = AttachedWarehouseSerializer()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "approved_at",
            "order_origin",
            "reference",
            "warehouse",
            "status",
        ]


class StatusPurchaseSerializer(serializers.ModelSerializer):

    id = IntegerField()
    created_at = DateTimeField()
    created_by = EmployeeSerializer()
    status = SimpleStatusSerializer()

    def to_representation(self, obj):
        """Move fields from status to purchase_status representation."""
        representation = super().to_representation(obj)
        status_representation = representation.pop("status")
        representation["status"] = status_representation["name"]
        return representation

    class Meta:
        model = PurchaseStatus
        fields = ["id", "purchase", "status", "created_by", "created_at"]


class SavePurchaseStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseStatus
        fields = ["id", "purchase", "status", "created_by", "created_at"]


class PurchaseAditionalInfoSerialzier(serializers.ModelSerializer):
    """
    Purchase Serializer that contains the list of purchase_childs ids and a list of all related purchase_status.
    """

    childs = serializers.SerializerMethodField(read_only=True)
    status_list = serializers.SerializerMethodField(read_only=True)
    warehouse = AttachedWarehouseSerializer()
    status = CharField()
    order_origin = AttachedOrderRequestSerializer()

    def get_childs(self, instance):
        qs = PurchaseChild.objects.filter(purchase_header=instance)
        return PurchaseChildSerializer(qs, many=True).data

    def get_status_list(self, instance):
        qs = PurchaseStatus.objects.filter(purchase=instance).order_by("created_at")
        return StatusPurchaseSerializer(qs, many=True).data

    class Meta:
        model = Purchase
        fields = "__all__"
