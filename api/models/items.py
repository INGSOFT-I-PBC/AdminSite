from django.db import models
from .common import StatusModel, TimestampModel
from .users import Employee
from django.core.validators import MinValueValidator


class CategoryModel(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    description = models.CharField(max_length=256)
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)
    name = models.CharField(max_length=60)
    short_name = models.CharField(max_length=15)

    # Tiemstamp model parameter not needed
    deleted_at = None

    class Meta:
        db_table = "category"


class CategoryParamsModel(models.Model):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT)
    default_value = models.CharField(max_length=100)
    field = models.CharField(max_length=50, blank=False, null=False)
    field_type = models.CharField(max_length=20, blank=False, null=False)
    required = models.BooleanField(default=False)

    class Meta:
        db_table = "category_params"


class ItemsModel(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)

    brand = models.CharField(max_length=128)
    category = models.ForeignKey(CategoryModel, on_delete=models.RESTRICT)
    created_by = models.ForeignKey(Employee, on_delete=models.RESTRICT)
    img = models.CharField(max_length=255)
    iva = models.DecimalField(default=0, max_digits=6, decimal_places=3)
    model = models.CharField(max_length=128)
    name = models.CharField(max_length=60)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=14, decimal_places=3
    )
    status = models.ForeignKey(StatusModel, on_delete=models.RESTRICT)

    class Meta:
        db_table = "items"


class ItemMetaDataModel(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)

    item = models.ForeignKey(ItemsModel, on_delete=models.RESTRICT)
    param = models.ForeignKey(CategoryParamsModel, on_delete=models.RESTRICT)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "item_meta_data"
