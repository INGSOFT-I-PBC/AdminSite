from django.core.validators import MinValueValidator
from django.db import models

from api.models.common import Status
from api.models.invoice import Invoice
from api.models.items import Item
from api.models.orders import OrderRequest
from api.models.products import Product, ProductVariant
from api.models.provider import Provider
from api.models.users import Employee
from api.models.warehouse import Warehouse


class Purchase(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    approved_at = models.DateTimeField(null=False, auto_now_add=True)
    order_origin = models.ForeignKey(OrderRequest, on_delete=models.RESTRICT, null=True)
    reference = models.IntegerField(unique=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT)

    class Meta:
        db_table = "purchase"


class PurchaseChild(models.Model):

    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)
    purchase_header = models.ForeignKey(Purchase, on_delete=models.RESTRICT)
    invoice = models.ForeignKey(
        Invoice, null=True, default=None, on_delete=models.RESTRICT
    )
    provider = models.ForeignKey(Provider, on_delete=models.RESTRICT)
    img_details = models.CharField(max_length=255, null=True)
    is_purchased = models.BooleanField(default=False, null=False, blank=False)
    is_delivered = models.BooleanField(default=False, null=False, blank=False)
    comment = models.CharField(max_length=300, null=True, blank=True)

    class Meta:

        db_table = "purchase_child"


class PurchaseDetail(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)
    purchase_child = models.ForeignKey(PurchaseChild, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.RESTRICT)
    product = models.ForeignKey(Product, on_delete=models.RESTRICT)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=15
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["product", "variant", "purchase_child"]]
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

    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)

    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    purchase = models.ForeignKey(Purchase, on_delete=models.RESTRICT)

    class Meta:
        db_table = "purchase_status"
