from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import CharField, IntegerField, BooleanField
from rest_framework.validators import UniqueValidator

from api.models import Employee


class EmployeeSerializer(ModelSerializer):

    id = IntegerField()
    name = CharField(max_length=128)
    lastname = CharField(max_length=128)
    cid = CharField(
        max_length=11, validators=[UniqueValidator(queryset=Employee.objects.all())]
    )
    # role = models.ForeignKey("Role", on_delete=models.CASCADE)
    is_active = BooleanField()

    class Meta:
        model = Employee
        fields = ["id", "name", "lastname", "cid", "is_active"]
