from django.db import models

from api.models.common import StatusModel
from api.models.items import ItemsModel

from .wharehouse import WharehouseModel
from .provider import ProviderModel
from .orders import OrderStatusModel
from .invoice import InvoiceDetailsModel
from .users import Employee
from django.core.validators import MinValueValidator


class PurchaseModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    provider = models.ForeignKey(ProviderModel, on_delete=models.RESTRICT)
    order_origin = models.ForeignKey(
        OrderStatusModel, on_delete=models.RESTRICT, null=True
    )
    reference = models.IntegerField()
    wharehouse = models.ForeignKey(WharehouseModel, on_delete=models.RESTRICT)
    invoice = models.ForeignKey(InvoiceDetailsModel, on_delete=models.RESTRICT)
    img_details = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "purchase"


class PurchaseDetailsModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    purchase = models.ForeignKey(PurchaseModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    price = models.DecimalField(validators=[MinValueValidator(0)], decimal_places=3, max_digits=15)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "purchase_details"


class PurchaseStatusModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)
    purchase = models.ForeignKey(PurchaseModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "purchase_status"
