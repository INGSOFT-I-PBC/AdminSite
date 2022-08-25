from django.db import models
from .wharehouse import WharehouseModel
from .common import StatusModel
from .users import Employee
from .items import ItemsModel
from django.core.validators import MinValueValidator


class OrderRequestModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    requested_at = models.DateTimeField(null=False, auto_now_add=True)
    requested_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
    )
    wharehouse = models.ForeignKey(WharehouseModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "order_request"


class OrderRequestDetailsModel(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    order_request = models.ForeignKey(OrderRequestModel, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "order_request_details"


class OrderStatusModel(models.Model):

    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)
    order = models.ForeignKey(OrderRequestModel, on_delete=models.RESTRICT)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "order_status"
