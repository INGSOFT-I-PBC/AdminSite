from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, IntegerField, DateTimeField

from api.models.common import Status
from .users import Employee, EmployeeSerializer


class StatusSerializer(ModelSerializer):

    id = IntegerField()
    name = CharField(max_length=255)
    description = CharField(max_length=255)
    created_by = EmployeeSerializer()

    class Meta:
        model = Status
        fields = ["id", "name", "description", "created_by"]
