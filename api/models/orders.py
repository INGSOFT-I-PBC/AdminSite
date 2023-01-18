from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from api.models.products import ProductVariant

from .common import Status
from .items import Item
from .users import Employee
from .warehouse import Warehouse


class OrderRequest(models.Model):
    class OrderStatus(models.TextChoices):
        PENDING_APPROVAL = "PA", _("Pendiente aprobacion")
        CREATED = "CR", _("Creado")
        CANCELED = "CA", _("Cancelado")
        CHANGES_NEEDED = "CN", _("Cambios necesarios")
        APPROVED = "AP", _("Aprobado")
        NEGATED = "NG", _("Negada")

    requested_at = models.DateTimeField(null=False, auto_now_add=True)
    requested_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        db_column="requested_by",
        related_name="requested_by",
    )
    revised_at = models.DateTimeField(null=True, default=None)
    revised_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
        db_column="revised_by",
        related_name="revised_by",
        default=None,
        null=True,
    )
    warehouse = models.ForeignKey(
        Warehouse, on_delete=models.RESTRICT, related_name="warehouse"
    )
    comment = models.CharField(
        max_length=512, default="", help_text="Comentario adicional al pedido"
    )
    status = models.CharField(
        max_length=6, choices=OrderStatus.choices, default=OrderStatus.PENDING_APPROVAL
    )

    class Meta:
        db_table = "order_request"
        indexes = [models.Index(fields=["status"])]


class OrderRequestDetail(models.Model):

    order_request = models.ForeignKey(
        OrderRequest, on_delete=models.CASCADE, related_name="items"
    )
    item = models.ForeignKey(
        ProductVariant, on_delete=models.RESTRICT, related_name="ordered_on"
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "order_request_details"


class OrderStatus(models.Model):
    order = models.ForeignKey(OrderRequest, on_delete=models.RESTRICT)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)

    class Meta:
        db_table = "order_status"
