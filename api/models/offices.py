from django.db import models
from .common import Status


class BranchOffice(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    created_at = models.DateTimeField(null=False, auto_now_add=True)
    name = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        db_table = "branch_offices"
        indexes = [
            models.Index(fields=["name"]),
        ]
