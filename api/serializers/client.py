#from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers


from api.models import Client, Gender,Province,City

class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ['id', 'name', 'short_name']
class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name', 'short_name']
class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ['id', 'name', 'short_name']


class FullClientSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """
    gender = GenderSerializer()
    city= GenderSerializer()
    province= GenderSerializer()
    class Meta:
        model = Client
        fields = [
            'id',
            'created_at',
            'updated_at',
            'deleted_at',
            'address',
            'business_name',
            'email',
            'number_id',
            'name',
            'phone_number',
            'city',
            'created_by_id',
            'gender',
            'province',
            'status_id'
        ]



class ClientSerializer(serializers.ModelSerializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """
    #gender = GenderSerializer()
    class Meta:
        model = Client
        fields = [
            'created_at',
            'updated_at',
            'deleted_at',
            'address',
            'business_name',
            'email',
            'number_id',
            'name',
            'phone_number',
            'city_id',
            'created_by_id',
            'gender_id',
            'province_id',
            'status_id'
        ]
