from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Status
from api.serializers import StatusSerializer
from rest_framework.permissions import IsAuthenticated
from api.utils import error_response
from django.http import JsonResponse

class StatusView(APIView):
    """
    This View holds multiple methods for the client
    """
    permission_classes = (IsAuthenticated,)


    def get(self, request: Request):
        try:
            name = str(request.GET.get('name'))
           # "Status.objects.get(name="active")"
            status= Status.objects.filter(name=name).first()
            if  status is None:
                return error_response('Not found', status=404)
            serializer =StatusSerializer(status)
            return JsonResponse(serializer.data)
        except TypeError:
            return error_response('invalid params')

