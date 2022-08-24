from django.db import models
from .common import StatusModel, TimestampModel
from .users import Employee
from .items import ItemsModel
from django.core.validators import MinValueValidator


class WharehouseModel(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=128)

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "wharehouse"


class InventoryModel(TimestampModel):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    wharehouse = models.ForeignKey(WharehouseModel, on_delete=models.RESTRICT)
    item = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    delete_at = None

    updated_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)

    class Meta:
        db_table = "inventory"


class WharehouseTransactionModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    notes = models.CharField(max_length=300, blank=True)
    wharehouse_origin = models.ForeignKey(
        WharehouseModel, on_delete=models.RESTRICT, related_name="origin"
    )
    wharehouse_destiny = models.ForeignKey(
        WharehouseModel, on_delete=models.RESTRICT, related_name="destiny"
    )
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "wharehouse_transaction"


class WhTransactionDetailsModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    header = models.ForeignKey(WharehouseTransactionModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    class Meta:
        db_table = "wh_transaction_details"
