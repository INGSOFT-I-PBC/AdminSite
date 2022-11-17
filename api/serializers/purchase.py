from rest_framework import serializers
from rest_framework.fields import CharField

from api.models import Purchase
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
