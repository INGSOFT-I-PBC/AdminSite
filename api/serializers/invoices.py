# from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers
from django.core.validators import MinValueValidator
import rest_framework.serializers as _srl


from api.models import (
    Category,
    Client,
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

class ISimpleProductSerializer(_srl.ModelSerializer):
    id = _srl.IntegerField()
    product_name = _srl.CharField(max_length=128)
    brand_name = _srl.CharField(max_length=50)
    base_price = _srl.DecimalField(max_digits=14, decimal_places=3)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "brand_name",
            "base_price",
        ]
class ISimpleVariantSerializer(ModelSerializer):

    id = IntegerField()
    variant_name = _srl.CharField(max_length=50)
    sku = _srl.CharField(max_length=128)
    price = _srl.DecimalField(max_digits=14, decimal_places=3)
    is_active = _srl.BooleanField()

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "variant_name",
            "sku",
            "price",
            "is_active",
        ]

class IProductStockSerializer(ModelSerializer):

    id = IntegerField()
    variant = ISimpleVariantSerializer()
    product = ISimpleProductSerializer()
    stock_level = IntegerField()

    class Meta:
        model = ProductStockWarehouse
        fields = ["id","product", "variant", "stock_level"]

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

    category = ICategorySerializer(read_only=True)

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

'''class IInventorySerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    item = IItemSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = [
            "id",
            "item",
            "quantity"
        ]'''

class IInventorySerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    variant = ISimpleVariantSerializer(read_only=True)

    class Meta:
        model = ProductStockWarehouse
        fields = [
            "id",
            "variant",
            "stock_level"
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


class IPayMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaymentMethod
        fields = ["id", "name"]


class IInvoiceDetailsSerializer(serializers.ModelSerializer):
    variant = ISimpleVariantSerializer()
    product=ISimpleProductSerializer()

    class Meta:
        model = InvoiceDetails
        fields = ["id", "invoice", "price", "quantity","variant","product"]


class IInvoiceDetailsEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = ["id", "invoice", "price", "quantity","variant","product"]

'''class InvoiceInventorySerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a Invoice Inventary model object
    """
    id=serializers.IntegerField(read_only=True)
    item=serializers.PrimaryKeyRelatedField(read_only=True)
    quantity=serializers.IntegerField(validators=[MinValueValidator(0)])


    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        #print(instance)

        instance.save()
        return instance

'''
class InvoiceInventorySerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a Invoice Inventary model object
    """
    id=serializers.IntegerField(read_only=True)
    stock_level=serializers.IntegerField(validators=[MinValueValidator(0)])


    def update(self, instance, validated_data):
        instance.stock_level = validated_data.get("stock_level", instance.stock_level)
        #print(instance)

        instance.save()
        return instance

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
class InvoiceSerializerlist(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = [
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
