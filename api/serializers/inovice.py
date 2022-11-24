from rest_framework.serializers import ModelSerializer

from api.models.invoice import Invoice


class SimpleInvoiceSerializer(ModelSerializer):
    class Meta:
        model = Invoice
        fields = ["id", "code", "created_at"]
