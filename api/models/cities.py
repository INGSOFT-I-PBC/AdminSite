from pyexpat import model
from django.db import models


class Province(models.Model):
    """
    This model represent a province.

    Args:
        models (Model): A Django's Model.

    Attributes:
        name(CharField):
            The name of the province
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "provinces"
        indexes = [
            models.Index(
                fields=[
                    "name",
                ],
                name="idx_prov_name_find",
            )
        ]


class City(models.Model):
    """
    This model represent a city with the needed Data for internal transaction or
    documents.

    Args:
        models (Model): A Django's Model

    Attributes:
        name(CharField):
            The name of the city that the `instance` refer.

        short_name (CharField):
            An internal way to identify a city with a shortname.

        province (Province):
            The province in which the city belongs to.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    province = models.ForeignKey(Province, on_delete=models.RESTRICT)

    class Meta:
        db_table = "cities"
        indexes = [
            models.Index(
                fields=[
                    "name",
                ],
                name="idx_city_name",
            ),
            models.Index(
                fields=[
                    "short_name",
                ],
                name="idx_short_name",
            ),
        ]
