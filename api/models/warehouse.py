from django.core.validators import MinValueValidator
from django.db import models

from api.models.common import Status, TimestampModel
from api.models.items import Item
from api.models.users import Employee


class Warehouse(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    name = models.CharField(max_length=128)

    latitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=6, null=True)

    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    def __str__(self):
        return f"Warehouse '{self.name}'"

    class Meta:
        db_table = "warehouse"
        indexes = [
            models.Index(fields=["name"]),
        ]


class Inventory(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT)
    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])

    delete_at = None

    updated_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)

    def __str__(self):
        return f"Inventory of '{self.warehouse.name}'"

    class Meta:
        db_table = "inventory"

    def nombreItem(self):
        return self.item.name

    def created_at_Item(self):
        return self.item.created_at

    def brandItem(self):
        return self.item.brand

    def imgItem(self):
        return self.item.img.name
        # imgItem

    def ivaItem(self):
        return self.item.iva

    def modelItem(self):
        return self.item.model

    def priceItem(self):
        return self.item.price

    def category_id_Item(self):
        return self.item.category_id

    def category_name_Item(self):
        return self.item.category.name

    def created_by_Item(self):
        return {
            "created_by": self.item.created_by.id,
            "name": self.item.created_by.name,
            "lastname": self.item.created_by.lastname,
        }

    def status_id_Item(self):
        return self.item.status_id

    def codename_Item(self):
        return self.item.codename

    def is_active(self):
        return self.item.is_active


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
    variant = models.ForeignKey("ProductVariant", on_delete=models.RESTRICT)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    quantity = models.IntegerField()

    class Meta:
        db_table = "wh_transaction_details"


class WarehouseBarcode(models.Model):
    """WarehouseBarcode

    This class represent a record for a barcode stock inventory
    management, this should be only used for stock control and
    not for sale or other. Is designed to hold the information
    of the items and where it's supposed to be stored, additionally
    the order request, maybe associated to this item, can be added
    as additional information.

    Args:
        batch_no (CharField):
            This field holds the batch number that this barcode is
            related at.

        expiration_date (DateField):
            If this barcode has an expiration date, can be stored here.

        is_active (BooleanField):
            This control flag, checks if this range/single barcode are
            active or not. That means that if we want to update the barcode. We should update the

        serial_start (IntegerField):
            The start number of all the barcodes generated on an single
            record.

        serial_end (IntegerField):
            The end number of all the barcodes generated on a single
            record.

    """

    serial_start = models.PositiveBigIntegerField(null=False)

    serial_end = models.PositiveIntegerField(null=False)
    batch_no = models.CharField(max_length=32, editable=True, blank=False)

    label = models.CharField(blank=False, null=False, max_length=32)

    expiration_date = models.DateField(default=None, null=True)

    created_by = models.OneToOneField(
        Employee, related_name="associated_barcodes", on_delete=models.RESTRICT
    )

    updated_by = models.OneToOneField(
        Employee,
        related_name="updated_barcodes",
        default=None,
        null=True,
        on_delete=models.RESTRICT,
    )

    is_active = models.BooleanField(default=True, null=False)

    created_at = models.DateTimeField(null=False, editable=False, auto_now=True)

    updated_at = models.DateTimeField(null=True, editable=False, auto_now_add=True)

    warehouse = models.OneToOneField(
        Warehouse, related_name="stock_barcodes", null=False, on_delete=models.RESTRICT
    )

    order_request = models.OneToOneField(
        "OrderRequest", null=True, default=None, on_delete=models.RESTRICT
    )

    class Meta:
        db_table = "wh_stock_barcodes"


class WhBarcodeItems(models.Model):

    barcode = models.OneToOneField(
        WarehouseBarcode, on_delete=models.RESTRICT, null=False, related_name="content"
    )

    item = models.OneToOneField(
        Item, on_delete=models.RESTRICT, null=False, related_name="item"
    )

    quantity = models.PositiveIntegerField(null=False)

    class Meta:
        db_table = "wh_stock_barcode_content"


class TransactionStatus(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    transaction = models.ForeignKey(WarehouseTransaction, on_delete=models.RESTRICT)

    class Meta:
        db_table = "transaction_status"


class WhTomasFisicas(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    done_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    created_at = models.DateTimeField(null=False, auto_now_add=True)
    novedad = models.TextField(blank=True)
    warehouse = models.ForeignKey(Warehouse, on_delete=models.RESTRICT)

    class Meta:
        db_table = "tomas_fisicas"


class WhTomasFisicasDetails(models.Model):

    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    product = models.ForeignKey("Product", on_delete=models.RESTRICT)
    variant = models.ForeignKey("ProductVariant", on_delete=models.RESTRICT)
    toma_fisica = models.ForeignKey(WhTomasFisicas, on_delete=models.RESTRICT)
    novedad = models.CharField(max_length=300, null=False, blank=False)
    new_stock = models.PositiveIntegerField()
    previous_stock = models.PositiveIntegerField()

    class Meta:
        db_table = "tomas_fisicas_details"
