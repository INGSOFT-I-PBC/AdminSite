from django.core.validators import MinValueValidator
from django.db import models

from .common import Status
from .items import Item
from .users import Employee
from .warehouse import Warehouse



class OrderRequest(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    requested_at = models.DateTimeField(null=False, auto_now_add=True)
    requested_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="requested_by"
    )
    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT)
    comment = models.CharField(max_length=512, default="", help_text="Comentario adicional al pedido")

    class Meta:
        db_table = "order_request"


class OrderRequestDetail(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    order_request = models.ForeignKey(OrderRequest, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "order_request_details"


class OrderStatus(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)
    order = models.ForeignKey(OrderRequest, on_delete=models.RESTRICT)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "order_status"
