from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Sequence
from api.serializers import FullSequenceSerializer,SequenceSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from api.utils import error_response
from django.http import JsonResponse

class SequenceView(APIView):
    """
    This View holds multiple methods for the client
    """
    permission_classes = (IsAuthenticated,)


    def get(self, request: Request):
        try:
            name = request.GET.get('name')
            client = Sequence.objects.filter(name=name).first()
            if client is None:
                return error_response('Not found', status=404)
            serializer = SequenceSerializer(client)
            return JsonResponse(serializer.data)
        except TypeError:
            return error_response('invalid params')

    def put (self,request):
        name = request.GET.get('name')
        client=Sequence.objects.filter(name=name).first()
        serializer = SequenceSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass



class SequenceViewSet(ReadOnlyModelViewSet):
    queryset = Sequence.objects.all().order_by("name")
    serializer_class = FullSequenceSerializer




class FullSequenceViewSet(SequenceViewSet):
    pagination_class = None


'''class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = ClientSerializer'''



