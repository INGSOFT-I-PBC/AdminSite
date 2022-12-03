from rest_framework.serializers import (
    CharField,
    DateTimeField,
    DecimalField,
    IntegerField,
    ModelSerializer,
)

from api.models.products import InventoryProduct
from api.serializers.products import ProductVariantSerializer
from api.serializers.users import EmployeeSerializer as SimpleEmployeeSerializer


class ProductInventorySerializer(ModelSerializer):

    product = ProductVariantSerializer()
    quantity = IntegerField()
    updated_by = SimpleEmployeeSerializer()
    updated_at = DateTimeField()

    def to_representation(self, obj):
        """Move fields from prduct to inventory representation."""
        representation = super().to_representation(obj)
        product_representation = representation.pop("product")
        for key in product_representation:
            representation[key] = product_representation[key]

        return representation

    class Meta:
        model = InventoryProduct
        fields = ["product", "updated_by", "updated_at", "quantity"]
