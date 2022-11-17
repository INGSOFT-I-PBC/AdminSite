# from rest_framework.serializers import ModelSerializer
import rest_framework.serializers as serializers
from rest_framework.validators import UniqueValidator

from api.models import City, Client, Employee, Gender, Province, Status

# from api.serializers.status import StatusSerializer


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ["id", "name", "short_name"]


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ["id", "name", "short_name"]


class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Province
        fields = ["id", "name"]


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ["name", "lastname", "cid", "role"]


class FullClientSerializer(serializers.ModelSerializer):
    """
    Serializer class that show all the data of the Warehouse model
    """

    gender = GenderSerializer()
    city = CitySerializer()
    province = ProvinceSerializer()
    created_by = EmployeeSerializer()
    # status=StatusSerializer()
    class Meta:
        model = Client
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "address",
            "business_name",
            "email",
            "number_id",
            "name",
            "phone_number",
            "city",
            "created_by",
            "gender",
            "province",
            #'status'
        ]


class ClientSerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """

    id = serializers.IntegerField(read_only=True)
    address = serializers.CharField(max_length=256)
    business_name = serializers.CharField(max_length=128)
    email = serializers.EmailField(max_length=32)
    name = serializers.CharField(max_length=60)
    number_id = serializers.CharField(
        max_length=16,
        validators=[
            UniqueValidator(
                queryset=Client.objects.all(), message=("El número de cédula ya existe")
            )
        ],
    )
    phone_number = serializers.CharField(max_length=16)
    city = serializers.PrimaryKeyRelatedField(queryset=City.objects.all())
    created_by = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all())
    gender = serializers.PrimaryKeyRelatedField(queryset=Gender.objects.all())
    province = serializers.PrimaryKeyRelatedField(queryset=Province.objects.all())
    status = serializers.PrimaryKeyRelatedField(queryset=Status.objects.all())

    def create(self, validated_data):
        return Client.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.address = validated_data.get("address", instance.address)
        instance.business_name = validated_data.get(
            "business_name", instance.business_name
        )
        instance.email = validated_data.get("email", instance.email)
        instance.number_id = validated_data.get("number_id", instance.number_id)
        instance.name = validated_data.get("name", instance.name)
        instance.phone_number = validated_data.get(
            "phone_number", instance.phone_number
        )
        instance.city = validated_data.get("city", instance.city)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.gender = validated_data.get("gender", instance.gender)
        instance.province = validated_data.get("province", instance.phone_number)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance
