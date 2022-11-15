# from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers

from api.models import (
    Category,
    Client,
    Employee,
    Invoice,
    InvoiceDetails,
    Item,
    PaymentMethod,
)


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["name", "lastname", "cid", "role"]


class ICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class IItemSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    category = ICategorySerializer()

    class Meta:
        model = Item
        fields = [
            "id",
            "codename",
            "brand",
            "iva",
            "model",
            "name",
            "price",
            "category",
        ]


class IClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "business_name",
            "email",
            "number_id",
            "name",
        ]


class IPayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]


class IInvoiceDetailsSerializer(serializers.ModelSerializer):
    item = IItemSerializer()

    class Meta:
        model = InvoiceDetails
        fields = ["id", "invoice", "item", "price", "quantity", "price"]


class IInvoiceDetailsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = ["id", "invoice", "item", "price", "quantity", "price"]


class FullInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Invoice model
    """

    payment_method = IPayMethodSerializer()
    client = IClientSerializer()
    # created_by=EmployeeSerializer()
    invoice_details = IInvoiceDetailsSerializer(many=True)

    class Meta:
        model = Invoice
        fields = [
            "id",
            "client",
            "code",
            "created_at",
            "iva",
            "return_deadline",
            "emission",
            "payment_method",
            "status",
            "subtotal",
            "total",
            "anulated",
            #'created_by',
            "invoice_details",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "client",
            "code",
            "created_at",
            "emission",
            "return_deadline",
            "iva",
            "payment_method",
            "status",
            "subtotal",
            "total",
            "anulated",
            "created_by",
        ]


class InvoiceEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
            "client",
            "created_at",
            "emission",
            "return_deadline",
            "iva",
            "payment_method",
            "status",
            "subtotal",
            "total",
            "anulated",
            "created_by",
        ]
