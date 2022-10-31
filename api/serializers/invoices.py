#from rest_framework.serializers import ModelSerializer
from asyncore import read
from http import client
import rest_framework.serializers as serializers
from rest_framework.validators import UniqueValidator


from api.models import Client,Employee,Status, PaymentMethod,Invoice,InvoiceDetails,City,Province,Gender

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['name','lastname','cid','role']
class IClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
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
            'created_at',
            'iva',
            'payment_method',
            'status',
            'subtotal',
            'total',
            'anulated',
            'created_by',
            'invoice_details']







class InvoiceSerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """
    id=serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=256)
    business_name = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=32)
    name = serializers.CharField(max_length=60)
    number_id = serializers.CharField(max_length=16,validators=[UniqueValidator(queryset=Client.objects.all(),message=("El número de cédula ya existe"))])
    phone_number = serializers.CharField(max_length=16)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    status= serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address", instance.address)
        instance.business_name = validated_data.get("business_name", instance.business_name)
        instance.email = validated_data.get("email", instance.email)
        instance.number_id = validated_data.get("number_id", instance.number_id)
        instance.name = validated_data.get("name", instance.name)
        instance.phone_number = validated_data.get("phone_number", instance.phone_number)
        instance.city = validated_data.get("city", instance.city)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.province = validated_data.get("province", instance.phone_number)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
