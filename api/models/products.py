from django.db import models

from api.models.common import TimestampModel
from api.utils import PathAndRename

from .provider import Provider


class Product(TimestampModel):

    product_name = models.CharField(max_length=128, null=False, blank=False)

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

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["product_name"]),
            models.Index(fields=["short_description"]),
        ]


class ProductMeta(models.Model):
    """Product Meta

    This class represents all the common meta data associated to a given product without
    considering the variant of the given product.

    Attributes:
        product (Product):
            This is the product that owns this property/param.

        name (CharField):
            This is the name of the given meta data.

        value (CharField):
            This is the value of this meta data
    """

    product = models.ForeignKey(
        Product, related_name="common_props", on_delete=models.RESTRICT
    )

    name = models.CharField(max_length=50, null=False, blank=False)

    value = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        db_table = "product_meta"
        indexes = [models.Index(fields=["name"]), models.Index(fields=["value"])]


class ProductVariant(TimestampModel):

    product = models.ForeignKey(
        Product, related_name="variants", on_delete=models.RESTRICT
    )

    variant_name = models.CharField(max_length=50, null=False, blank=False)

    sku = models.CharField(
        max_length=128, null=False, blank=False, help_text="The Stock Keeping Unit code"
    )

    price = models.DecimalField(max_digits=20, decimal_places=3, null=False, default=0)

    active = models.BooleanField(default=True, null=False)

    img = models.ImageField(upload_to=PathAndRename("products"), null=True, blank=True)

    def _delete_resources(self):
        obj = None
        try:
            obj = ProductVariant.objects.get(id=self.pk)
        except ProductVariant.DoesNotExist:
            return  # If there is not registry of prev avoid
        if obj is not None and self.img != obj.img:
            obj.img.delete()  # delete previous image

    def save(self, *args, **kwargs):
        self._delete_resources()
        return super(ProductVariant, self).save(*args, **kwargs)

    class Meta:
        db_table = "products_variant"
        indexes = [
            models.Index(fields=["variant_name"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["price"]),
        ]


class VariantMeta(models.Model):

    variant = models.ForeignKey(
        ProductVariant, related_name="meta", on_delete=models.RESTRICT
    )
    name = models.CharField(max_length=60, blank=False, null=False)
    value = models.CharField(max_length=60, blank=False, null=False)

    class Meta:
        db_table = "product_variant_meta"
        indexes = [models.Index(fields=["name"]), models.Index(fields=["value"])]


class ProductProviders(models.Model):
    product = models.ForeignKey(
        ProductVariant, related_name="providers", on_delete=models.RESTRICT
    )

    provider = models.ForeignKey(
        Provider, related_name="provided_products", on_delete=models.RESTRICT
    )
    active = models.BooleanField(default=True, null=False, blank=False)

    class Meta:
        db_table = "product_providers"
