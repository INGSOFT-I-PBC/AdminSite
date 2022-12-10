from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import OuterRef, Prefetch, Q, Subquery
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Inventory, OrderRequest, Warehouse
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
    WarehouseSerializer,
    WhInventorySerializer,
    WhStockSerializer,
    WhTransactionSerializer,
    WhWithTomaFisicaSerializer,
)
from api.utils import error_response, response


class CustomPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "page": self.page.number,
                "lastPage": self.page.paginator.num_pages,
                "total": self.page.paginator.count,
            }
        )


class WarehouseView(APIView):
    """
    This View holds multiple methods for the Warehouse
    """

    def get(self, request: Request):

        try:

            querydict = request.query_params

            filters = {}

            for key, value in querydict.items():
                if key in ["id", "name", "latitude", "longitude"]:
                    filters[key] = value

            warehouse_qset = Warehouse.objects.filter(**filters)

            warehouse_qset = warehouse_qset.exclude(status__name="invalid").latest("id")

            serializer = WarehouseSerializer(warehouse_qset)

            return JsonResponse(serializer.data)

        except Exception as e:
            error_response("Invalid query")

    def put(self, request: Request):

        try:

            queryid = request.query_params.get("id")

            data = dict(**request.data)

            warehouse = Warehouse.objects.get(id=queryid)

            serializer = WarehouseSerializer(warehouse, data=data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return JsonResponse({"error": False, "message": serializer.data})

        except Exception as e:
            error_response("Invalid query")

    def post(self, request: Request):

        data = dict(**request.data)

        try:

            valid_status = Status.objects.get(name="active")

            data["status"] = valid_status.id

            serializer = WarehouseSerializer(data=data)

            serializer.is_valid(raise_exception=True)

            serializer.update()

        except Exception as e:
            error_response("Invalid query")

        return JsonResponse({"error": False, "message": "Ok"})

    def delete(self, request: Request):
        """
        This method would deactivate a warehouse.
        Args:
            request: The Request

        Returns:
            A response with the status information about the action
            executed.

        """
        try:
            querydict = request.query_params

            filters = {}

            for key, value in querydict.items():
                if key in ["id", "name", "latitude", "longitude"]:
                    filters[key] = value

            filters["status"] = Status.objects.get(name="active")

            inactive_status = Status.objects.get(name="inactive")

            updateted_rows = Warehouse.objects.filter(**filters).update(
                status=inactive_status
            )

            return JsonResponse(
                {"error": False, "message": "Rows affected: " + str(updateted_rows)},
            )

        except Exception as e:

            error_response("Invalid query")


class WarehouseViewSet(ReadOnlyModelViewSet):

    queryset = Warehouse.objects.all().order_by("name").exclude(status__name="inactive")
    serializer_class = FullWarehouseSerializer


class FullWarehouseViewSet(WarehouseViewSet):
    pagination_class = None


class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = OrderSerializer(queryset, many=True)

    def list(self, request):

        page_number = request.query_params.get("page")

        if page_number:

            paginator = Paginator(self.queryset, 50)

            page_obj = paginator.get_page(page_number)

            return Response(OrderSerializer(page_obj, many=True).data)

        return Response(self.serializer_class.data)


class WhStockViewSet(ModelViewSet):
    pagination_class = CustomPagination
    queryset = ProductStockWarehouse.objects.all().order_by("-id")
    serializer_class = WhStockSerializer

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


class WhOrderRequestView(APIView):
    def get(self, request):

        try:

            wh_orders = OrderRequest.objects.filter(
                warehouse__pk=request.query_params.get("id")
            ).order_by("-id")

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(
                    wh_orders, request.query_params.get("per_page", 15)
                )

                page_obj = paginator.get_page(page_number)

                return JsonResponse(
                    {
                        "data": OrderSerializer(page_obj, many=True).data,
                        "total": paginator.count,
                        "page": int(page_number),
                        "lastPage": paginator.num_pages,
                    }
                )

            return Response(OrderSerializer(wh_orders, many=True).data)

        except:
            return error_response("Invalid query")


class WhTransactionViewSet(ModelViewSet):

    queryset = WarehouseTransaction.objects.all().order_by("-created_at")
    serializer_class = WhTransactionSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset.select_related("created_by", "status")
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("id", None):
            queryset = queryset.filter(id=params.get("id"))
            return queryset

        if params.get("warehouse_id", None):

            if params.get("entrada", None) and params.get("salida", None):
                queryset = queryset.filter(
                    Q(warehouse_destiny=params.get("warehouse_id"))
                    | Q(warehouse_origin=params.get("warehouse_id"))
                )
            elif params.get("entrada", None):
                queryset = queryset.filter(warehouse_destiny=params.get("warehouse_id"))
            elif params.get("salida", None):
                queryset = queryset.filter(warehouse_origin=params.get("warehouse_id"))

        if params.get("warehouse_name", None):

            if params.get("entrada", None) and params.get("salida", None):
                queryset = queryset.filter(
                    Q(warehouse_destiny__name__icontains=params.get("warehouse_name"))
                    | Q(warehouse_origin__name__icontains=params.get("warehouse_name"))
                )

            elif params.get("entrada", None):
                queryset = queryset.filter(
                    warehouse_destiny__name__icontains=params.get("warehouse_name")
                )

            elif params.get("salida", None):
                queryset = queryset.filter(
                    warehouse_origin__name__icontains=params.get("warehouse_name")
                )

        if params.get("from_date", None):
            queryset = queryset.filter(created_at__gte=(params.get("from_date")))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)
            queryset = queryset.filter(created_at__lte=to_date)

        if params.get("notes", None):
            queryset = queryset.filter(notes__icontains=(params.get("from_date")))

        if params.get("created_by", None):
            queryset = queryset.filter(created_by=(params.get("created_by")))

        if params.get("created_by_name", None):
            queryset = queryset.filter(
                created_by__name__icontains=(params.get("created_by_name"))
            )
            queryset = queryset.filter(
                created_by__lastname__icontains=(params.get("created_by_name"))
            )

        return queryset


class WhTransactionDetailsViewSet(ModelViewSet):
    queryset = WarehouseTransaction.objects.all()
    serializer_class = TranactionWithProductsSerializer

    def get_queryset(self):

        queryset = self.queryset.select_related(
            "created_by", "status"
        ).prefetch_related("wh_transaction_details")
        params = self.request.query_params.copy()

        if (not params.get("id", False)) and (not params.get("warehouse_id", False)):
            return error_response("Invalid request")

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("id", None):
            queryset = queryset.filter(id=params.get("id"))
            return queryset

        if params.get("warehouse_id", None):

            if params.get("entrada", None) and params.get("salida", None):
                queryset = queryset.filter(
                    Q(warehouse_destiny=params.get("warehouse_id"))
                    | Q(warehouse_origin=params.get("warehouse_id"))
                )

            elif params.get("entrada", None):
                queryset = queryset.filter(
                    warehouse_destiny__name__icontains=params.get("warehouse_name")
                )

            elif params.get("salida", None):
                queryset = queryset.filter(
                    warehouse_origin__name__icontains=params.get("warehouse_name")
                )

        return queryset


class WhOrderRequestViewSet(ReadOnlyModelViewSet):
    """
    API Endpoint that allows only read operation on the given Orders that are registered and available
    """

    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = OrderSerializer(queryset, many=True)


class WhLatestTomaFisicaView(APIView):
    def get(self, request):
        try:

            latest_tf = WhTomasFisicas.objects.filter(
                warehouse=OuterRef("id")
            ).order_by("-id")[:1]

            wh_with_toma_fisica = Warehouse.objects.annotate(
                whtf_id=Subquery(latest_tf.values("id")),
                whtf_created_at=Subquery(latest_tf.values("created_at")),
                whtf_novedad=Subquery(latest_tf.values("novedad")),
                whtf_done_by_name=Subquery(latest_tf.values("done_by__name")),
                whtf_done_by_lastname=Subquery(latest_tf.values("done_by__lastname")),
            ).order_by("name")

            serializer = WhWithTomaFisicaSerializer(wh_with_toma_fisica, many=True)

            return Response(serializer.data)

        except Exception as e:
            return error_response("Invalid query")


class TomasFisicasDetailsViewSet(ModelViewSet):
    queryset = WhTomasFisicasDetails
    serializer_class = FullTomasDetailSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset.objects.order_by("id")
        params = self.request.query_params.copy()
        print(params)
        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("toma_fisica", None):
            queryset = queryset.filter(
                toma_fisica__id=params.get("toma_fisica")
            ).select_related("product", "variant")
            return queryset

        return error_response("Invalid request")


class WhTomasFisicasViewSet(ModelViewSet):

    queryset = WhTomasFisicas.objects.all().order_by("-created_at")
    serializer_class = TomasFisicasSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).select_related("warehouse", "done_by")

        if params.get("employee_name", None):
            queryset = queryset.filter(
                done_by__name__icontains=params.get("employee_name")
            )

        if params.get("employee_id", None):
            queryset = queryset.filter(done_by__id=params.get("employee_id"))

        if params.get("novedad", None):
            queryset = queryset.filter(novedad__icontains=params.get("novedad"))

        if params.get("from_date", None):
            queryset = queryset.filter(created_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)
            queryset = queryset.filter(created_at__lte=to_date)

        return queryset

    def create_toma_fisica(self, request):

        data = request.data
        data["done_by"] = request.user.employee_id
        tomas_serializer = SimpleTomasFisicasSerializer(
            data=data,
        )
        details = request.data.pop("details", None)
        # There were no details givem, toma had no issues
        if not details or len(details) == 0:

            try:
                tomas_serializer.is_valid(raise_exception=True)
                tomas_serializer.save()
                return response("Toma Física created")
            except Exception as e:
                return error_response("Data is not valid")

        if tomas_serializer.is_valid(raise_exception=True):

            details = [x for x in details if x]
            toma_fisica: WhTomasFisicas = tomas_serializer.save()
            for detail in details:
                detail["toma_fisica"] = toma_fisica.pk

            details_serializer = TomasDetailSerializer(data=details, many=True)

            try:
                details_serializer.is_valid(raise_exception=True)

            except Exception as e:
                toma_fisica.delete()
                raise e
            details_serializer.save()
            serializer = TomasFisicasSerializer(toma_fisica)
            return JsonResponse(serializer.data, status=201)
        return error_response("Data is not valid")
