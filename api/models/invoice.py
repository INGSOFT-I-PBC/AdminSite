from django.db import models

from api.models.items import ItemsModel
from .common import StatusModel
from .clients import ClientModel
from .users import Employee
from .offices import BranchOfficeModel
from django.core.validators import MinValueValidator


class PaymentMethodModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    name = models.CharField(max_length=50)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "payment_method"


class CreditNote(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    branch_office_id = models.ForeignKey(BranchOfficeModel, on_delete=models.RESTRICT)
    client_id = models.ForeignKey(ClientModel, on_delete=models.RESTRICT)
    code = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.ForeignKey(
        Employee,
        on_delete=models.RESTRICT,
    )
    iva = models.DecimalField(max_digits=6, decimal_places=3)
    payment_method = models.ForeignKey(PaymentMethodModel, on_delete=models.RESTRICT)
    return_deadline = models.DateField()
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)
    subtotal = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=14
    )
    total = models.DecimalField(decimal_places=3, max_digits=14)

    class Meta:
        db_table = "credit_note"


class InvoiceModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    code = models.CharField(max_length=128, blank=False)
    client_id = models.ForeignKey(ClientModel, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    credit_note_id = models.ForeignKey(CreditNote, null=True, on_delete=models.RESTRICT)
    iva = models.DecimalField(max_digits=6, decimal_places=3)
    payment_method = models.ForeignKey(PaymentMethodModel, on_delete=models.RESTRICT)
    return_deadline = models.DateField()
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)
    subtotal = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=15
    )
    transaction_code = models.CharField(max_length=128, null=True)
    total = models.DecimalField(decimal_places=3, max_digits=15)

    class Meta:
        db_table = "invoice"


class InvoiceDetailsModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    invoice_id = models.ForeignKey(InvoiceModel, on_delete=models.RESTRICT)
    item_id = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=14
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "invoice_details"
