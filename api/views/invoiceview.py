from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Invoice,Client
from api.serializers.invoices import  FullInvoiceSerializer,IClientSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from api.utils import error_response
from django.http import JsonResponse
from rest_framework.decorators import action

class InvoiceView(viewsets.GenericViewSet):

    @action(methods=['get'], detail=False)
    def search_client(self, request:Request):
        ruc_or_business_name = request.GET.get('number_id')
        supplier = Client.objects.filter(
           number_id=ruc_or_business_name
        ).first()
        print(supplier)
        if supplier:
            supplier_serializer = IClientSerializer(supplier)
            return Response(supplier_serializer.data, status=status.HTTP_200_OK)
        return Response({
            'mensaje': 'No se ha encontrado un Cliente.'
        }, status=status.HTTP_400_BAD_REQUEST)

class ClientView(APIView):
    """
    This View holds multiple methods for the client
    """
    permission_classes = (IsAuthenticated,)


    def get(self, request: Request):
        try:
            id = int(request.GET.get('id'))
            client = Client.objects.filter(pk=id).first()
            if client is None:
                return error_response('Not found', status=404)
            serializer = ClientSerializer(client)
            return JsonResponse(serializer.data)
        except TypeError:
            return error_response('invalid params')

    def post(self, request):
        serializer = ClientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def put (self,request):
        id = int(request.GET.get('id'))
        client=Client.objects.filter(pk=id).first()
        serializer = ClientSerializer(client, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        pass

    def delete(self, request):

        """
        This method would deactivate a client.
        Args:
            request: The Request

        Returns:
            A response with the status information about the action
            executed.

        """
        try:
            id = int(request.GET.get('id'))
            client = Client.objects.filter(pk=id).first()
            if client is None:
                return error_response('Not found', status=404)
            client.delete()
            return Response('OK',status=status.HTTP_200_OK)
        except TypeError:
            return error_response('invalid params')



class InvoiceViewSet(ReadOnlyModelViewSet):
    queryset = Invoice.objects.all().order_by("id")
    serializer_class = FullInvoiceSerializer




class FullInvoiceViewSet(InvoiceViewSet):
    pagination_class = None


'''class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = ClientSerializer'''



