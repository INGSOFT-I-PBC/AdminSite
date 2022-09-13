from django.db import models
from .common import Status, TimestampModel
from .users import Employee
from .items import Item
from django.core.validators import MinValueValidator


class Warehouse(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=128)

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        db_table = "warehouse"


class Inventory(TimestampModel):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    delete_at = None

    updated_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)

    class Meta:
        db_table = "inventory"


class WarehouseTransaction(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    notes = models.CharField(max_length=300, blank=True)
    warehouse_origin = models.ForeignKey(
        Warehouse, on_delete=models.RESTRICT, related_name="origin"
    )
    warehouse_destiny = models.ForeignKey(
        Warehouse, on_delete=models.RESTRICT, related_name="destiny"
    )
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        db_table = "warehouse_transaction"


class WhTransactionDetails(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    header = models.ForeignKey(WarehouseTransaction, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    class Meta:
        db_table = "wh_transaction_details"
