# from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers
from django.core.validators import MinValueValidator
import rest_framework.serializers as _srl


from api.models import (
    Category,
    Client,
    CreditNote,
    Employee,
    Invoice,
    InvoiceDetails,
    Item,
    ProductVariant,
    Product,
    ProductStockWarehouse,
    PaymentMethod,Inventory
)

from rest_framework.serializers import (
    DateTimeField,
    IntegerField,
    ModelSerializer,
)
from api.serializers.users import EmployeeSerializer as SimpleEmployeeSerializer
from api.models.products import ProductStockWarehouse


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["name", "lastname", "cid", "role"]

class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "business_name",
            "email",
            "number_id",
            "name",
        ]
class PayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]

class CreditNoteListSerializer(ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    created_by = EmployeeSerializer(read_only=True)
    client=  ClientSerializer(read_only=True)
    payment_method=  PayMethodSerializer(read_only=True)

    class Meta:
        model = CreditNote
        fields = ["id","code", "created_at","created_by", "client","iva","payment_method","return_deadline","active","subtotal","total"]

class CreditNoteSerializer(ModelSerializer):

    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = CreditNote
        fields = ["id","code", "created_at","created_by", "client","iva","payment_method","return_deadline","active","subtotal","total"]

class CreditNoteInvoiceSerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a Invoice Inventary model object
    """
    id=serializers.IntegerField(read_only=True)
    anulated=serializers.BooleanField()
    credit_note=serializers.PrimaryKeyRelatedField(queryset=CreditNote.objects.all())

    def update(self, instance, validated_data):
        instance.anulated = validated_data.get("anulated", instance.anulated)
        instance.credit_note = validated_data.get("credit_note", instance.credit_note)

        print (instance)
        instance.save()
        return instance
