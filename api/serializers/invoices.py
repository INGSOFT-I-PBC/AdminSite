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
<<<<<<< HEAD


class IPayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]

=======
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27


class IPayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]


class IInvoiceDetailsSerializer(serializers.ModelSerializer):
    item = IItemSerializer()

    class Meta:
        model = InvoiceDetails
<<<<<<< HEAD
        fields = "__all__"
=======
        fields = ["id", "invoice", "item", "price", "quantity", "price"]


class IInvoiceDetailsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = ["id", "invoice", "item", "price", "quantity", "price"]
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27


class FullInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Invoice model
    """

    payment_method = IPayMethodSerializer()
    client = IClientSerializer()
<<<<<<< HEAD
    created_by = EmployeeSerializer()
=======
    # created_by=EmployeeSerializer()
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27
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
<<<<<<< HEAD
            "created_by",
=======
            #'created_by',
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27
            "invoice_details",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
<<<<<<< HEAD
            "id",
            "code",
=======
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
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27
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
