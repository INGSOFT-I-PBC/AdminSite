#from rest_framework.serializers import ModelSerializer
from asyncore import read
import rest_framework.serializers as serializers



from api.models import Sequence

class FullSequenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sequence
        fields = '__all__'

class SequenceSerializer(serializers.Serializer):
    """
    Serializer class that show the essential data of a warehouse model object
    """
    id=serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    number = serializers.IntegerField()

    def create(self, validated_data):
        return Sequence.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.number = validated_data.get("number", instance.number)
        instance.save()
        return instance

