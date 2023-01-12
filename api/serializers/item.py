from distutils.command.install_data import install_data

import rest_framework.serializers as serializers

from api.models import Category, ItemMetaData
from api.models.items import Item
from api.serializers.status import StatusSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["description", "name", "short_name"]


class ItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Item
        fields = (
            "id",
            "codename",
            "brand",
            "img",
            "iva",
            "model",
            "name",
            "price",
            "category",
        )


class DetailedItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class SimpleItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    brand = serializers.CharField(max_length=128)
    img = serializers.CharField(max_length=255)
    iva = serializers.DecimalField(max_digits=6, decimal_places=3)
    model = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=60)
    price = serializers.DecimalField(max_digits=14, decimal_places=3)
    codename = serializers.CharField(max_length=128)

    category = CategorySerializer()
    status = StatusSerializer()

    def create(self, validated_data):
        return Item(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.brand = validated_data.get("brand", instance.brand)
        instance.img = validated_data.get("img", instance.img)
        instance.iva = validated_data.get("iva", instance.iva)
        instance.model = validated_data.get("model", instance.model)
        instance.name = validated_data.get("name", instance.name)
        instance.price = validated_data.get("price", instance.price)
        instance.codename = validated_data.get("codename", instance.codename)

        return instance

    class Meta:
        model = Item
        fields = "__all__"


class ItemPriceSerializer(serializers.Serializer):
    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.price = validated_data.get("price", instance.price)
        instance.save()
        return instance


class ItemPropSerializer(serializers.RelatedField):
    name = serializers.CharField(max_length=256)
    value = serializers.CharField(max_length=256)

    def to_internal_value(self, data):
        """
        Not used read only serializer
        :param data: the data to transform
        :return: null
        """
        return None

    def to_representation(self, meta: ItemMetaData):
        raw_value = meta.value
        fallback = meta.param.default_value
        return {
            "name": meta.param.field,
            "type": meta.param.field_type,
            "value": fallback if raw_value is None else raw_value,
        }

    def get_queryset(self):
        return ItemMetaData.objects.all()


class MetaDataSerializer(serializers.Serializer):
    value = serializers.CharField()

    def create(self, validated_data):
        return ItemMetaData(**validated_data)

    def update(self, instance, validated_data):
        instance.id = validated_data.get("id", instance.id)
        instance.item = validated_data.get("item", instance.item)
        instance.param = validated_data.get("param", instance.param)
        instance.value = validated_data.get("value", instance.value)


class FullItemSerializer(ItemSerializer):
    properties = ItemPropSerializer(
        many=True, read_only=True, source="itemmetadata_set"
    )
