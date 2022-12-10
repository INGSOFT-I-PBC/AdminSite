import rest_framework.serializers as _srl

from api.models import Product, ProductAttribute, ProductVariant


class SimpleAttributeSerializer(_srl.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "value", "type"]


class ProductVariantSerializer(_srl.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = "__all__"


class _SimpleProductVariant(_srl.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "variant_name", "sku", "price", "img"]


class ProductSerializer(_srl.ModelSerializer):

    variants = _srl.SerializerMethodField(read_only=True)
    # attributes = SimpleAttributeSerializer(many=True, required=False)
    attributes = _srl.SerializerMethodField(read_only=True)

    def get_variants(self, product):
        qs = ProductVariant.objects.filter(is_active=True)
        return _SimpleProductVariant(instance=qs, many=True).data

    def get_attributes(self, instance):
        qs = ProductAttribute.objects.filter(product=instance, option=None)
        return SimpleAttributeSerializer(qs, many=True).data

    class Meta:
        model = Product
        fields = "__all__"


class ProductAttributeSerializer(_srl.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = "__all__"


class AttachedAttributeSerializer(_srl.ModelSerializer):
    class Meta:
        model = ProductAttribute
        fields = ["name", "value", "type"]


class InputProductSerializer(_srl.ModelSerializer):
    class InputVariantSerializer(_srl.ModelSerializer):
        sku = _srl.CharField(read_only=True, max_length=128)
        attributes = AttachedAttributeSerializer(many=True, required=False)

        def create(self, validated_data):
            attribute_data = validated_data.pop("attributes", None)
            variant = ProductVariant.objects.create(**validated_data)
            attribute_serializer = self.fields["attributes"]
            # save attributes if present
            if attribute_data:
                for each in attribute_data:
                    each["product"] = variant.product
                    each["option"] = variant
                print("the attribute value is:")
                attribute_serializer.create(attribute_data)
            return variant

        class Meta:
            model = ProductVariant
            fields = [
                # "product",
                "variant_name",
                "sku",
                "price",
                "img",
                "stock_level",
                "attributes",
            ]

    variants = InputVariantSerializer(many=True, required=False)
    attributes = AttachedAttributeSerializer(many=True, required=False)

    def create(self, validated_data):
        variant_data = validated_data.pop("variants", None)
        attribute_data = validated_data.pop("attributes", None)
        product = Product.objects.create(**validated_data)
        att_serializer = self.fields["attributes"]
        var_serializer = self.fields["variants"]
        # Save the data for nested things
        if variant_data:
            for each in variant_data:
                each["product"] = product
            var_serializer.create(variant_data)
        if attribute_data:
            for each in attribute_data:
                each["product"] = product
            att_serializer.create(attribute_data)
        return product

    class Meta:
        model = Product
        fields = [
            "product_name",
            "summary",
            "short_description",
            "brand_name",
            "base_price",
            "categories",
            "variants",
            "attributes",
        ]


class AttachedVMeta(_srl.Serializer):
    """Attached Variant Meta
    This class represent the metadata that is attached on a given

    Args:
        _srl (Serializer): The Serializer parent class
    """


class AttachedVariant(_srl.Serializer):
    """Attached Product Variant
    This class is a serializer used when creating a product that can have
    attached their variants already as list.

    Args:
        Serializer (class): Serializer parent class
    """

    variant_name = _srl.CharField(
        max_length=50, allow_null=False, allow_blank=False, required=True
    )

    sku = _srl.CharField(
        max_length=128, allow_null=False, allow_blank=False, required=True
    )
    # If price is not present then inherit the product base price
    price = _srl.DecimalField(
        max_digits=20,
        decimal_places=3,
        allow_null=True,
        default=0,
        required=False,
    )

    img = _srl.ImageField(required=False)


class CplxProductSerializer(_srl.Serializer):
    pass


class DataProdVariantSerializer(_srl.Serializer):
    product = _srl.PrimaryKeyRelatedField(
        queryset=Product.objects.filter(is_active=True), allow_null=False
    )
    variant_name = _srl.CharField(allow_null=True, allow_blank=True, max_length=50)
    sku = _srl.CharField(allow_null=False, allow_blank=False, max_length=128)
    price = _srl.DecimalField(max_digits=20, decimal_places=3, allow_null=False)
    img = _srl.ImageField(required=False)


class SimpleProductSerializer(_srl.ModelSerializer):
    id = _srl.IntegerField()
    product_name = _srl.CharField(max_length=128)
    summary = _srl.CharField()
    short_description = _srl.CharField(max_length=256)
    brand_name = _srl.CharField(max_length=50)
    base_price = _srl.DecimalField(max_digits=14, decimal_places=3)

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


class ProductVariantSerializer(_srl.ModelSerializer):

    id = _srl.IntegerField()
    created_at = _srl.DateTimeField()
    updated_at = _srl.DateTimeField()
    deleted_at = _srl.DateTimeField()
    variant_name = _srl.CharField(max_length=50)
    sku = _srl.CharField(max_length=128)
    price = _srl.DecimalField(max_digits=14, decimal_places=3)
    is_active = _srl.BooleanField()
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
            "is_active",
            "product",
        ]


class SimpleVariantSerializer(_srl.ModelSerializer):

    id = _srl.IntegerField()
    created_at = _srl.DateTimeField()
    updated_at = _srl.DateTimeField()
    deleted_at = _srl.DateTimeField()
    variant_name = _srl.CharField(max_length=50)
    sku = _srl.CharField(max_length=128)
    price = _srl.DecimalField(max_digits=14, decimal_places=3)
    is_active = _srl.BooleanField()

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
            "is_active",
        ]
