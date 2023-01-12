from rest_framework import serializers

from api.models import Employee, Item, OrderRequest, OrderRequestDetail, Warehouse
from api.models.products import ProductProvider
from api.serializers.auth import EmployeeSerializer
from api.serializers.item import SimpleItemSerializer
from api.serializers.product import ProductVariantSerializer
from api.serializers.provider import PartialProviderSerializer


class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"


class PartialOrderSerializer(serializers.Serializer):
    requested_at = serializers.DateTimeField(allow_null=True, required=False)
    requested_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=False
    )

    revised_by = serializers.PrimaryKeyRelatedField(
        queryset=Employee.objects.all(), required=False, allow_null=True
    )
    revised_at = serializers.DateTimeField(allow_null=True, required=False)

    warehouse = serializers.PrimaryKeyRelatedField(
        queryset=Warehouse.objects.all(), required=False, allow_null=False
    )

    comment = serializers.CharField(
        allow_null=False, allow_blank=True, max_length=512, required=False
    )

    status = serializers.ChoiceField(
        choices=OrderRequest.OrderStatus.choices,
        allow_null=False,
        required=False,
    )

    def update(self, instance: OrderRequest, validated_data):
        instance.revised_by = validated_data.get("revised_by", instance.revised_by)
        instance.revised_at = validated_data.get("revised_at", instance.revised_at)
        instance.warehouse = validated_data.get("warehouse", instance.warehouse)
        instance.comment = validated_data.get("comment", instance.comment)
        instance.status = validated_data.get("status", instance.status)
        instance.save()
        return instance


class OrderDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderRequestDetail
        fields = ("order_request", "item", "quantity")


class _Item(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Item
        fields = ("brand", "name", "category")


class _DetailSerializer(serializers.ModelSerializer):
    item_name = serializers.CharField(source="item.name")
    item_category = serializers.CharField(source="item.category.name")
    item_brand = serializers.CharField(source="item.brand")

    class Meta:
        model = OrderRequestDetail
        fields = ("quantity", "item_name", "item_category", "item_brand")


class OrderReadSerializer(serializers.ModelSerializer):
    requested_by = EmployeeSerializer()
    revised_by = EmployeeSerializer()
    items = _DetailSerializer(read_only=True, many=True)
    warehouse = serializers.CharField(source="warehouse.name")

    class Meta:
        model = OrderRequest
        fields = "__all__"


class OrderDetailSerializerprueba(serializers.ModelSerializer):
    # item = SimpleItemSerializer()
    item = ProductVariantSerializer()

    class Meta:
        model = OrderRequestDetail
        fields = ["order_request", "item", "quantity"]


class OrderDetailProviderProductSerializer(serializers.ModelSerializer):
    product = ProductVariantSerializer()
    provider = PartialProviderSerializer()

    class Meta:
        model = ProductProvider
        fields = ["product", "provider", "price"]


class OrderSerializerORDREQ(serializers.ModelSerializer):
    class Meta:
        model = OrderRequest
        fields = "__all__"

    def to_representation(self, instance):
        return {
            "id": instance.id,
            "requested_at": instance.requested_at,
            "requested_by": instance.requested_by.name,
            "warehouse": instance.warehouse.name,
            "warehouse_id": instance.warehouse.id,
        }


class InputOrderSerializer(serializers.Serializer):
    pass
