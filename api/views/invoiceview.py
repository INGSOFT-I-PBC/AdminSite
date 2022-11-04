from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Invoice,Client,Item
from api.serializers.invoices import  FullInvoiceSerializer,IClientSerializer,IItemSerializer,IInvoiceDetailsSerializer,InvoiceSerializer
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from api.utils import error_response
from django.http import JsonResponse
from rest_framework.decorators import action
import datetime


class PaginatedIItemViewSet(ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = IItemSerializer

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
    @action(methods=['post'], detail=False)
    def save_invoice(self, request:Request):
        if not request.data:
            return error_response("No data was provided")
        items = request.data.pop("invoice_details")
        items = [x for x in items if x]
        if not items:
            return error_response("An order need at least one item")

        data = request.data
        data["created_by"] = request.user.employee_id
        data["created_at"] = datetime.datetime.now()
        serializer = InvoiceSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            order: Invoice = serializer.save()
            for item in items:
                # inject order, due client doesn't know which is created
                item["invoice"] = order.pk
            item_serializer = IInvoiceDetailsSerializer(data=items, many=True)
            try:  # Check if the inserted items are valid
                item_serializer.is_valid(raise_exception=True)
            except Exception as e:
                order.delete()
                raise e
            item_serializer.save()
            serializer = InvoiceSerializer(order)
            return JsonResponse(serializer.data)
        return error_response("The given data was invalid")




class InvoiceViewSet(ReadOnlyModelViewSet):
    queryset = Invoice.objects.all().order_by("id")
    serializer_class = FullInvoiceSerializer




class FullInvoiceViewSet(InvoiceViewSet):
    pagination_class = None




'''class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = ClientSerializer'''



