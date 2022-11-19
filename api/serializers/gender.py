import rest_framework.serializers as serializers

from api.models import Gender


class GenderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gender
        fields = ["id", "name", "short_name"]
