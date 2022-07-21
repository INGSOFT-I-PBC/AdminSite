from django.db import models


class Employee(models.Model):
    id = models.AutoField(primary_key=True, editable=False, auto_created=True)
    name = models.CharField(max_length=128, null=False)
    lastname = models.CharField(max_length=128, null=False)
    cid = models.CharField(max_length=11, unique=True)
    role = models.ForeignKey("Role", on_delete=models.CASCADE)
    created_at = models.DateTimeField(null=False, auto_now=True, editable=False)
    is_active = models.BooleanField(null=False, default=True)

    class Meta:
        db_table = "employees"
