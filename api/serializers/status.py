#from rest_framework.serializers import ModelSerializer
from asyncore import read
import rest_framework.serializers as serializers


from api.models import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']
