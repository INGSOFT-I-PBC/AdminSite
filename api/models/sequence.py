from dataclasses import field
from pyexpat import model
from django.db import models

class Sequence(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=150, unique=True)
    number = models.IntegerField(null=True)

    class Meta:
        db_table = "sequence"



