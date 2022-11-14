from rest_framework import serializers

from api.models import Purchase, PurchaseStatus
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
            "img_details",
            "invoice",
            "provider",
            "order_origin",
            "reference",
            "warehouse",
        ]


class PurchaseStatusSerializer(serializers.ModelSerializer):

    status = StatusSerializer()

    def to_representation(self, obj):
        """Move fields from status to purchase representation."""
        representation = super().to_representation(obj)
        item_representation = representation.pop("status")
        for key in item_representation:
            representation[key] = item_representation[key]

        return representation

    def to_internal_value(self, data):
        """Move fields related to status to their own status dictionary."""
        status_internal = {}
        for key in StatusSerializer.Meta.fields:
            if key in data:
                status_internal[key] = data.pop(key)

        internal = super().to_internal_value(data)
        internal["status"] = status_internal
        return internal

    #   def update(self, instance, validated_data): Needs to update status related object

    class Meta:
        model = PurchaseStatus
        filed = ["created_at", "created_by", "status"]
