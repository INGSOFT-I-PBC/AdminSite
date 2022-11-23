from django.forms import DateTimeField, IntegerField
from rest_framework import serializers
from rest_framework.fields import CharField

from api.models import Purchase
from api.models.purchases import PurchaseStatus
from api.serializers.auth import EmployeeSerializer
from api.serializers.common import StatusSerializer
from api.serializers.inovice import SimpleInvoiceSerializer
from api.serializers.provider import SimpleProviderSerializer


class PurchaseSerializer(serializers.ModelSerializer):

    invoice = SimpleInvoiceSerializer()
    provider = SimpleProviderSerializer()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "aproved_at",
            "img_details",
            "invoice",
            "provider",
            "order_origin",
            "reference",
            "warehouse",
        ]


class PurchaseStatusSerializer(serializers.ModelSerializer):

    status = CharField()
    invoice = SimpleInvoiceSerializer()
    provider = SimpleProviderSerializer()

    class Meta:
        model = Purchase
        fields = [
            "id",
            "aproved_at",
            "img_details",
            "invoice",
            "provider",
            "order_origin",
            "reference",
            "warehouse",
            "status",
        ]


class StatusPurchaseSerializer(serializers.ModelSerializer):

    id = IntegerField()
    created_at = DateTimeField()

    def create(self, validated_data):
        return PurchaseStatus.objects.create(**validated_data)

    class Meta:
        model = PurchaseStatus
        fields = ["id", "purchase", "status", "created_by", "created_at"]
