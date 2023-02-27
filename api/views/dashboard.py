from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import OuterRef, Prefetch, Q, Subquery
from rest_framework.decorators import action
from datetime import datetime
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework import status, viewsets

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Inventory, OrderRequest, Warehouse,Invoice,InvoiceDetails
from api.models.common import Status
from api.models.products import ProductStockWarehouse, ProductVariant
from api.models.warehouse import (
    WarehouseTransaction,
    WhTomasFisicas,
    WhTomasFisicasDetails,
)
from api.serializers.order import OrderSerializer
from api.serializers.warehouse import (
    FullTomasDetailSerializer,
    FullWarehouseSerializer,
    SimpleTomasFisicasSerializer,
    TomasDetailSerializer,
    TomasFisicasSerializer,
    TranactionWithProductsSerializer,

    WhInventorySerializer,
    WhStockSerializer,
    WhTransactionSerializer,
    WhWithTomaFisicaSerializer,
)
from api.serializers.invoices import (FullInvoiceSerializer,InvoiceSerializer,InvoiceSerializerlist)
from api.utils import error_response, response

class DashboardViewSet(viewsets.GenericViewSet):

    @action(methods=["get"], detail=False)
    def search_sales(self, request: Request):
        fecha_final = datetime.now().date()

        fecha_inicio = datetime(fecha_final.year, fecha_final.month, 1).date()
        dias=obtener_dias_del_mes(2,2019)
        print(dias)
        print(fecha_inicio)
        print(fecha_final)
        if fecha_inicio:
            items=Invoice.objects.filter(
            emission__gte=fecha_inicio,
            emission__lte=fecha_final).aggregate(Sum('total'))
            print(items)
            #supplier_serializer = InvoiceSerializerlist(items, many=True)
            return Response(items, status=status.HTTP_200_OK)
        return Response(
            {"mensaje": "No se ha encontrado el facturas."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    @action(methods=["get"], detail=False)
    def search_sales_months(self, request: Request):
        fecha_final = datetime.now().date()
        fecha_iniciop = datetime(2023, 2, 25).date()

        fecha_inicio = datetime(fecha_final.year, fecha_final.month, 1).date()


        print(fecha_inicio)
        print(fecha_final)
        dias=obtener_dias_del_mes(2,2019)
        print(dias)
        i = 1
        dict={}
        if fecha_iniciop:
            while i <= fecha_iniciop.month:
                print(i)

                fecha_fina= datetime(fecha_iniciop.year, i, obtener_dias_del_mes(i,fecha_iniciop.year)).date()
                fecha_inici=datetime(fecha_iniciop.year, i, 1).date()
                items=Invoice.objects.filter(
                emission__gte=fecha_inici,
                emission__lte=fecha_fina).aggregate(Sum('total'))
                dict[str(i)]=items['total__sum']
                print(dict)
                i += 1
            return Response(dict, status=status.HTTP_200_OK)

        '''if fecha_inicio:
            items=Invoice.objects.filter(
            emission__gte=fecha_inicio,
            emission__lte=fecha_final).aggregate(Sum('total'))
            print(items)
            #supplier_serializer = InvoiceSerializerlist(items, many=True)
            return Response(items, status=status.HTTP_200_OK)'''
        return Response(
            {"mensaje": "No se ha encontrado el facturas."},
            status=status.HTTP_400_BAD_REQUEST,
        )
def es_bisiesto(anio: int) -> bool:
    return anio % 4 == 0 and (anio % 100 != 0 or anio % 400 == 0)


def obtener_dias_del_mes(mes: int, anio: int) -> int:
        # Abril, junio, septiembre y noviembre tienen 30
        if mes in [4, 6, 9, 11]:
            return 30
        # Febrero depende de si es o no bisiesto
        if mes == 2:
            if es_bisiesto(anio):
                return 29
            else:
                return 28
        else:
            # En caso contrario, tiene 31 días
            return 31

'''
    def get_queryset(self):
        queryset = self.queryset.select_related("product", "variant").filter(
            variant__is_active=True
        )
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("id", None):
            queryset = queryset.filter(id=params.get("id", None))
            return queryset

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse_id=params.get("warehouse_id")
            ).prefetch_related("variant", "product")

        if params.get("name", None):
            queryset = queryset.filter(
                Q(variant__variant_name__icontains=params.get("name"))
                | Q(product__product_name__icontains=params.get("name"))
            )

        if params.get("sku", None):
            queryset = queryset.filter(variant__sku__icontains=params.get("sku"))

        if params.get("min_quantity", None):
            queryset = queryset.filter(stock_level__gte=params.get("min_quantity"))

        if params.get("max_quantity", None):
            queryset = queryset.filter(stock_level__lte=params.get("max_quantity"))

        if params.get("min_price", None):
            queryset = queryset.filter(variant__price__gte=params.get("min_price"))

        if params.get("max_price", None):
            queryset = queryset.filter(variant__price__lte=params.get("max_price"))

        if params.get("from_date", None):
            queryset = queryset.filter(updated_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)

            queryset = queryset.filter(updated_at__lte=to_date)

        return queryset
'''

