#from rest_framework.serializers import ModelSerializer
from asyncore import read
from http import client
import rest_framework.serializers as serializers
from rest_framework.validators import UniqueValidator


from api.models import Client,Employee,Status, PaymentMethod,Item,Category,Invoice,InvoiceDetails,City,Province,Gender

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name','lastname','cid','role']
class ICategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name']

class IItemSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """
    category = ICategorySerializer()
    class Meta:
        model = Item
        fields = ['id', 'codename','brand', 'iva', 'model', 'name', 'price', 'category']

class IClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            'id',
            'business_name',
            'email',
            'number_id',
            'name',
        ]
class IPayMethodSerializer(serializers.ModelSerializer):
     class Meta:
        model = PaymentMethod
        fields = [
            'id',
            'name'
        ]

class IInvoiceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = InvoiceDetails
        fields = '__all__'

class FullInvoiceSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Invoice model
    """
    payment_method= IPayMethodSerializer()
    client= IClientSerializer()
    created_by=EmployeeSerializer()
    invoice_details=IInvoiceDetailsSerializer(many=True)
    class Meta:
        model = Invoice
        fields = [
            'id',
            'client',
            'code',
            'created_at',
            'iva',
            'return_deadline',
            'emission',
            'payment_method',
            'status',
            'subtotal',
            'total',
            'anulated',
            'created_by',
            'invoice_details']







class InvoiceSerializer(serializers.ModelSerializer):
     class Meta:
        model = Invoice
        fields = [
            'id',
            'code',
            'client',
            'created_at',
            'emission',
            'return_deadline',
            'iva',
            'payment_method',
            'status',
            'subtotal',
            'total',
            'anulated',
            'created_by',
            ]

