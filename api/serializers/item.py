from api.models.items import Item
import rest_framework.serializers as serializers


class ItemSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    brand = serializers.CharField(max_length=128)
    img = serializers.CharField(max_length=255)
    iva = serializers.DecimalField(max_digits=6, decimal_places=3)
    model = serializers.CharField(max_length=128)
    name = serializers.CharField(max_length=60)
    price = serializers.DecimalField(max_digits=14, decimal_places=3)

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

        return instance


class FullItemSerializer(serializers.Serializer):
    pass
