from dataclasses import field
from django.db import models
from .common import Status, TimestampModel
from .users import Employee
from django.core.validators import MinValueValidator


class Category(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    description = models.CharField(max_length=256)
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    name = models.CharField(max_length=60)
    short_name = models.CharField(max_length=15)

    # Tiemstamp model parameter not needed
    deleted_at = None

    class Meta:
        db_table = "category"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["description"]),
            models.Index(fields=["status"]),
        ]


class CategoryParam(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    default_value = models.CharField(max_length=100)
    field = models.CharField(max_length=50, blank=False, null=False)
    field_type = models.CharField(max_length=20, blank=False, null=False)
    required = models.BooleanField(default=False)

    class Meta:
        db_table = "category_params"
        indexes = [
            models.Index(fields=["field"]),
            models.Index(fields=["field_type"]),
            models.Index(fields=["required"]),
        ]


class Item(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    brand = models.CharField(max_length=128)
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    img = models.CharField(max_length=255)
    iva = models.DecimalField(default=0, max_digits=6, decimal_places=3)
    model = models.CharField(max_length=128)
    name = models.CharField(max_length=60)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=14, decimal_places=3
    )
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)

    class Meta:
        db_table = "items"
        indexes = [
            models.Index(fields=["name"], name="idx_item_name"),
            models.Index(fields=["price"], name="idx_item_price"),
            models.Index(fields=["category"], name="idx_item_category"),
            models.Index(fields=["brand"], name="idx_item_brand"),
        ]


class ItemMetaData(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)

    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    param = models.ForeignKey(CategoryParam, on_delete=models.RESTRICT)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "item_meta_data"
