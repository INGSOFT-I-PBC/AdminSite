from email.policy import default
from django.db import models

from api.models.items import Item
from .common import Status
from .clients import Client
from .users import Employee
from .offices import BranchOffice
from django.core.validators import MinValueValidator


class PaymentMethod(models.Model):
    """
    This model represents a Payment Method that is used internally for transactions.

    Args:
        models (Model): A Django's Model

    Attributes:
        name (CharField):
            The name of the payment method.

        status (Status):
            The status of the payment method.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    name = models.CharField(max_length=50)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        db_table = "payment_method"


class CreditNote(models.Model):
    """
    This model represents a credit note.

    Args:
        models (Model): A Django's Model

    Attributes:

    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    branch_office = models.ForeignKey(BranchOffice, on_delete=models.RESTRICT)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    code = models.CharField(max_length=128, blank=False)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    iva = models.DecimalField(max_digits=6, decimal_places=3)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT)
    return_deadline = models.DateField(null=True, default=None)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    subtotal = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=14
    )
    total = models.DecimalField(decimal_places=3, max_digits=14)
    anulated = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "credit_note"


class Invoice(models.Model):
    """
    This model represent an invoice

    Args:
        models (Model): A Django's Model.

    Attributes:

        code (CharField):
            The code of the invoce.

        client (Client):
            The client that owns the invoice.

        created_by (Employee):
            The creator of the Invoice.

        created_at (DateTimeField):
            The instant when the invoice was created.

        credit_note (CreditNote):
            The credit note (if needed) that refer to the invoice.

        iva (DecimalField):
            This field contains the value calculated for the IVA collected on the
            invoice.

        payment_method (PaymentMethod):
            The payment method used on this invoice.

        return_deadline (DateField):
            The date when is the limit when the invoice can be anulated or anything
            else.

        subtotal (DecimalField):
            The accumulated amount of money without taxes made on the invoice.

        total (DecimalField):
            The total money collected on the invoice.

        transaction_code (CharField):
            The code identifier for the payment transaction.

        anulated (BooleanField):
            A flag that represents if an Invoice is anulated.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    code = models.CharField(max_length=128, blank=False,unique=True)
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    credit_note = models.ForeignKey(CreditNote, null=True,default=None, on_delete=models.RESTRICT)
    iva = models.DecimalField(decimal_places=3, max_digits=15)
    payment_method = models.ForeignKey(PaymentMethod, on_delete=models.RESTRICT)
    return_deadline = models.DateField(null=True,default=None)
    emission = models.DateField(null=True,default=None)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    subtotal = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=15
    )
    transaction_code = models.CharField(max_length=128, null=True,default=None)
    total = models.DecimalField(decimal_places=3, max_digits=15)
    anulated = models.BooleanField(null=False, default=False)

    class Meta:
        db_table = "invoice"


class InvoiceDetails(models.Model):
    """
    This model represent the detail that an invoice holds, the items traded on a sale.

    Args:
        models (Model): A Django's Model.

    Attribute:
        invoice (Invoice):
            The header of the Invoice (master).

        item (Item):
            The item that is part of the sale.

        price (DecimalField):
            The price that the item was sold out.

        quantity (IntegerField):
            The quantity of items sold on this sale.
    """

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    invoice = models.ForeignKey(Invoice, related_name='invoice_details',on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], decimal_places=3, max_digits=14
    )
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        db_table = "invoice_details"
        indexes = [
            models.Index(fields=["item"]),
            models.Index(fields=["price"]),
            models.Index(fields=["quantity"]),
        ]
