from hashlib import sha1

from django.core.validators import MinValueValidator
from django.db import models

from api.mixins import AuditMixin, SoftDeleteMixin, TimestampMixin
from api.models.common import TimestampModel
from api.models.warehouse import Warehouse
from api.utils import PathAndRename

from .auth import Employee
from .provider import Provider


class Product(TimestampMixin, SoftDeleteMixin, AuditMixin, models.Model):
    """Product
    This is a product that would be used around all the system.

    Args:
        TimestampMixin (Model): Mixin that store the timestamps when a CRUD operation was performed
        SoftDeleteMixin (Model): Mixin that handle the delete method and set to false
        AuditMixin (Model): Mixin that handle a registry of who make a CRUD operation
        Models (Model): The base model of Django
    """

    product_name = models.CharField(
        max_length=128, null=False, blank=False, unique=True
    )

    summary = models.TextField(blank=True, null=False, default="")

    short_description = models.CharField(max_length=256, null=False, blank=False)

    brand_name = models.CharField(max_length=50, null=False, blank=False)

    base_price = models.DecimalField(
        max_digits=20,
        decimal_places=3,
        default=0,
        help_text="The base price or the common price for a product",
    )

    is_active = models.BooleanField(default=True, null=False)

    categories = models.ManyToManyField(
        "Category",
        through="ProductCategory",
        blank=True,
        related_name="listed_products",
    )

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["product_name"]),
            models.Index(fields=["short_description"]),
        ]


class ProductVariant(TimestampMixin, SoftDeleteMixin):

    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.RESTRICT
    )

    variant_name = models.CharField(max_length=50, null=False, blank=False)

    sku = models.CharField(
        max_length=128, null=False, blank=False, help_text="The Stock Keeping Unit code"
    )

    upc = models.CharField(max_length=13, null=True, blank=True, help_text="The UPC code of the Product variant")

    ean = models.CharField(max_length=13, null=True, blank=True)

    price = models.DecimalField(max_digits=20, decimal_places=3, null=False, default=0)

    img = models.ImageField(upload_to=PathAndRename("products"), null=True, blank=True)

    stock_level = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True, null=False)

    def _delete_resources(self):
        obj = None
        try:
            obj = ProductVariant.objects.get(id=self.pk)
        except ProductVariant.DoesNotExist:
            return  # If there is not registry of prev avoid
        if obj is not None and self.img != obj.img:
            obj.img.delete()  # delete previous image

    def _shorten(self, value: str):
        return sha1(value.encode("utf-8")).hexdigest()[0:5]

    def save(self, *args, **kwargs):
        super(ProductVariant, self).save(*args, **kwargs)
        self._delete_resources()
        if not self.sku:
            self.sku = "{:03}{:02}-{}{}-{}".format(
                self.product.pk,
                self.pk,
                self._shorten(self.product.product_name),
                self._shorten(self.variant_name),
                self._shorten(self.product.brand_name),
            )
            self.save()

    class Meta:
        db_table = "products_variant"
        indexes = [
            models.Index(fields=["variant_name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["price"]),
        ]
        unique_together = [["product", "variant_name"]]


class ProductAttribute(models.Model):
    """Product Attribute

    This class represents an attribute that an Product or a Product Option
    has related to, this are extra data associated to the given producta and
    are only for information.

    Attributes:
        product (Product):
            This is the product that owns this property/param.

        option (ProductOption):
            This is the product options that specifically is part to the
            product.

        name (CharField):
            This is the name of the given meta data.

        value (CharField):
            This is the value of this meta data
    """

    product = models.ForeignKey(
        Product, related_name="attributes", on_delete=models.RESTRICT
    )

    option = models.ForeignKey(
        ProductVariant, related_name="attributes", on_delete=models.RESTRICT, null=True
    )

    name = models.CharField(max_length=50, null=False, blank=False)

    value = models.CharField(max_length=50, null=False, blank=False)

    type = models.CharField(max_length=32, null=False, blank=False, default="string")

    class Meta:
        db_table = "product_attributes"
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["value"]),
        ]
        unique_together = [["option", "name"]]


class ProductProvider(models.Model):
    """ProductProvider
    This class is like a through table to get the providers that sell the given product, and hold the value that the provider sells that product

    Args:
        models (Model): The Django base model class
    """

    product = models.ForeignKey(
        ProductVariant, related_name="providers", on_delete=models.RESTRICT
    )

    provider = models.ForeignKey(
        Provider, related_name="provided_products", on_delete=models.RESTRICT
    )

    price = models.DecimalField(decimal_places=4, max_digits=20)
    active = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        db_table = "product_providers"


class ProductCategory(models.Model):
    """Product Category
    A transition table for Many to many relationship with products
    """

    product = models.ForeignKey(Product, related_name="+", on_delete=models.RESTRICT)

    category = models.ForeignKey(
        "Category", related_name="+", on_delete=models.RESTRICT
    )


class ProductStockWarehouse(TimestampMixin, SoftDeleteMixin, models.Model):
    product = models.ForeignKey(
        Product, related_name="warehouse_stock", on_delete=models.RESTRICT
    )

    variant = models.ForeignKey(
        ProductVariant,
        related_name="warehouse_stock",
        on_delete=models.RESTRICT,
        null=True,
        default=None,
    )

    warehouse = models.ForeignKey(
        "Warehouse",
        related_name="product_stock",
        on_delete=models.RESTRICT,
        help_text="The location where the stock is supposed",
    )

    updated_by = models.ForeignKey("Employee", on_delete=models.RESTRICT)

    stock_level = models.PositiveBigIntegerField(default=0)

    class Meta:
        db_table = "wh_product_stock"
        unique_together = [["product", "variant", "warehouse"]]
