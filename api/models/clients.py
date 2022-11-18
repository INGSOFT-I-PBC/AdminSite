from django.db import models

from api.models.cities import City, Province
from api.models.common import Status, TimestampModel
from api.models.genders import Gender
from api.models.users import Employee


class Client(TimestampModel):
    """
    This model represent a Client that use some service of the bussiness.

    Args:
        TimestampModel (Model): A Django's Model

    Attributes:
        address (CharField):
            This field contains the address info for the given client.

        business_name (CharField):
            This field represent the official name or the registered trademark that
            a client has.

        city (City):
            The city in where the client officialy makes their operations.

        email (EmailField):
            The email of the client.

        gender (Gender):
            The gender of the client.

        number_id (CharField):
            The identification of the client, might be ID-card number, passport, etc.

        phone_number (CharField):
            The phone number provided by the client.

        province (Province):
            The province of the address location.

        status (Status):
            The status of the client
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    address = models.CharField(max_length=256)
    business_name = models.CharField(null=True, max_length=128)
    city = models.ForeignKey(City, null=True, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    email = models.EmailField(max_length=32)
    gender = models.ForeignKey(Gender, null=True, on_delete=models.RESTRICT)
    number_id = models.CharField(max_length=12, unique=True)
    name = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=16)
    province = models.ForeignKey(Province, null=True, on_delete=models.RESTRICT)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    # Timestamp parameters created_at, updated_at, deleted_at

    class Meta:
        db_table = "clients"
        indexes = [
            models.Index(fields=["email"], name="idx_email"),
            models.Index(fields=["name"], name="idx_name"),
            models.Index(fields=["address"], name="idx_address"),
        ]
