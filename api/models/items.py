import datetime
import os
from dataclasses import field
from distutils.command.upload import upload

from django.core.validators import MinValueValidator
from django.db import models

from .common import Status, TimestampModel
from .users import Employee


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


def filepath(request, filename):
    old_filename = filename
    timeNow = datetime.datetime.now().strftime("%Y%m%d%H:%M:%S")
    filename = "%s%s" % (timeNow, old_filename)
    return os.path.join("uploads/", filename)


class Item(TimestampModel):
    id = models.AutoField(primary_key=True, auto_created=True, editable=False)
    brand = models.CharField(max_length=128)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, related_name="category"
    )
    created_by = models.ForeignKey(
        Employee, on_delete=models.RESTRICT, db_column="created_by"
    )
    img = models.ImageField(upload_to="storage/public/item", null=True, blank=True)
    iva = models.DecimalField(default=0, max_digits=6, decimal_places=3)
    model = models.CharField(max_length=128)
    name = models.CharField(max_length=60)
    price = models.DecimalField(
        validators=[MinValueValidator(0)], max_digits=14, decimal_places=3
    )
    status = models.ForeignKey(Status, on_delete=models.RESTRICT)
    codename = models.CharField(
        max_length=128, unique=True, help_text="The codename or identifier for the item"
    )
    is_active = models.BooleanField(null=False, default=True)


    class Meta:
        db_table = "items"
        indexes = [
            models.Index(fields=["name"], name="idx_item_name"),
            models.Index(fields=["price"], name="idx_item_price"),
            models.Index(fields=["category"], name="idx_item_category"),
            models.Index(fields=["brand"], name="idx_item_brand"),
        ]

    def remove_on_image_update(self):
        try:
            # is the object in the database yet?
            obj = Item.objects.get(id=self.id)
        except Item.DoesNotExist:
            # object is not in db, nothing to worry about
            return
        # is the save due to an update of the actual image file?
        if obj.img and self.img and obj.img != self.img:
            # delete the old image file from the storage in favor of the new file
            obj.img.delete()

    def save(self, *args, **kwargs):
        # object is possibly being updated, if so, clean up.
        self.remove_on_image_update()
        return super(Item, self).save(*args, **kwargs)


class ItemMetaData(models.Model):
    id = models.BigAutoField(primary_key=True, auto_created=True, editable=False)

    item = models.ForeignKey(Item, on_delete=models.RESTRICT)
    param = models.ForeignKey(CategoryParam, on_delete=models.RESTRICT)
    value = models.CharField(max_length=100)

    class Meta:
        db_table = "item_meta_data"
