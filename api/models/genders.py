from django.db import models


class Gender(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=30)
    short_name = models.CharField(max_length=6, null=True)

    class Meta:
        db_table = "genders"
