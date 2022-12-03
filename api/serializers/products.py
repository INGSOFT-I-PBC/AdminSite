from rest_framework.serializers import (
    BooleanField,
    CharField,
    DateTimeField,
    DecimalField,
    IntegerField,
    ModelSerializer,
)

from api.models.products import Product, ProductVariant, VariantMeta


class VariantPropSerializer(ModelSerializer):
    name = CharField(max_length=60)
    value = CharField(max_length=60)

    class Meta:
        model = VariantMeta
        fields = "__all__"


class SimpleProductSerializer(ModelSerializer):
    id = IntegerField()
    product_name = CharField(max_length=128)
    summary = CharField()
    short_description = CharField(max_length=256)
    brand_name = CharField(max_length=50)
    base_price = DecimalField(max_digits=14, decimal_places=3)

    class Meta:
        model = Product
        fields = [
            "id",
            "product_name",
            "summary",
            "short_description",
            "brand_name",
            "base_price",
        ]


class ProductVariantSerializer(ModelSerializer):

    id = IntegerField()
    created_at = DateTimeField()
    updated_at = DateTimeField()
    deleted_at = DateTimeField()
    variant_name = CharField(max_length=50)
    sku = CharField(max_length=128)
    price = DecimalField(max_digits=14, decimal_places=3)
    active = BooleanField()
    product = SimpleProductSerializer()

    def to_representation(self, obj):
        """Move fields from product to Vaariant representation."""
        representation = super().to_representation(obj)
        product_representation = representation.pop("product")
        for key in product_representation:
            if key == "id":
                representation["prod_id"] = product_representation[key]
            else:
                representation[key] = product_representation[key]

        return representation

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "created_at",
            "updated_at",
            "deleted_at",
            "variant_name",
            "sku",
            "price",
            "active",
            "product",
        ]
