from django.db import models

from api.models.common import Status
from api.models.items import Item

from .wharehouse import WharehouseModel
from .provider import Provider
from .orders import OrderStatus
from .invoice import InvoiceDetails
from .users import Employee
from django.core.validators import MinValueValidator


class Purchase(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT)
    order_origin = models.ForeignKey(OrderStatus, on_delete=models.RESTRICT, null=True)
    reference = models.IntegerField()
    wharehouse = models.ForeignKey(WharehouseModel, on_delete=models.RESTRICT)
    invoice = models.ForeignKey(InvoiceDetails, on_delete=models.RESTRICT)
    img_details = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = "purchase"


class PurchaseDetail(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    purchase = models.ForeignKey(Purchase, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=15
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "purchase_details"


class PurchaseStatus(models.Model):
    """
    Este modelo representa una tabla pivote que relaciona el estado de una compra con
    los estados disponibles en el sistema.

    Args:
        models (models.Model): Modelo Django

    Attributes:
        id (models.AutoField):
            Identificador del registro en la Base de Datos.
        created_by (Employee):
            El creador del registro.
        status (Status)
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    purchase = models.ForeignKey(Purchase, on_delete=models.RESTRICT)

    class Meta:
        db_table = "purchase_status"
