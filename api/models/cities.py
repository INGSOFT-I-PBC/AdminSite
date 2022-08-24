from django.db import models


class ProvinceModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=50)

    class Meta:
        db_table = "provinces"


class CitiesModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=5)
    province = models.ForeignKey(ProvinceModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "cities"
