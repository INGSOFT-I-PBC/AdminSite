from django.db import models
from .common import StatusModel, TimestampModel


class Employee(TimestampModel):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)

    name = models.CharField(max_length=128, null=False)
    lastname = models.CharField(max_length=128, null=False)

    cid = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT, null=True)

    class Meta:
        db_table = "employees"
