from django.db import models
from .common import TimestampModel, StatusModel
from .users import Employee
from .cities import CitiesModel, ProvinceModel


class GenderModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=6, null=True)

    class Meta:
        db_table = "genders"


class ClientModel(TimestampModel):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    address = models.CharField(max_length=256)
    business_name = models.CharField(null=True, max_length=128)
    city = models.ForeignKey(CitiesModel, null=True, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    email = models.EmailField(max_length=32)
    gender = models.ForeignKey(GenderModel, null=True, on_delete=models.RESTRICT)
    number_id = models.CharField(max_length=16)
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    province = models.ForeignKey(ProvinceModel, null=True, on_delete=models.RESTRICT)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    # Timestamp parameters created_at, updated_at, deleted_at

    class Meta:
        db_table = "clients"
