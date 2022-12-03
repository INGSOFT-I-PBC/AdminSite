from django.db import models

from api.models.common import TimestampModel
from api.models.genders import Gender


class Employee(TimestampModel):
    """
    This model represents an employee that is registered on the system.

    Args:
        TimestampModel (Model): A Django's Model.

    Attributes:
        name (CharField):
            The name of the employee.

        lastname (CharField):
            The lastname of the employee.

        cid (CharField):
            A document ID that provide an identifier for the employee

        role (Role):
            The role that the employee has on the bussiness.

        is_active (BooleanField):
            A flag that represent if an employee is active on the bussiness or not.

        phone_number (CharField):
            The phone number provided by the client.
    """

    id = models.AutoField(primary_key=True, editable=False, auto_created=True)

    name = models.CharField(max_length=128, null=False)
    lastname = models.CharField(max_length=128, null=False)

    cid = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    is_active = models.BooleanField(null=False, default=True)
    phone_number = models.CharField(max_length=16, null=True, default=None)
    created_by = models.ForeignKey(
        "self", on_delete=models.RESTRICT, default=None, null=True
    )
    gender = models.ForeignKey(Gender, null=True, on_delete=models.RESTRICT)
    address = models.CharField(max_length=256, null=True)

    class Meta:
        db_table = "employees"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["cid"]),
            models.Index(fields=["lastname"]),
        ]
