from rest_framework.serializers import ModelSerializer

from api.models import PaymentMethod


class FullPaymentSerializer(ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    class Meta:
        model = PaymentMethod
        fields = '__all__'


class PaymentSerializer(ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """
    class Meta:
        model = PaymentMethod
        fields = ['id','name']
