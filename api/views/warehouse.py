from django.core.paginator import Paginator
from django.db.models import OuterRef, Q, Subquery
from django.http import JsonResponse
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Inventory, OrderRequest, Purchase, PurchaseStatus, Warehouse
from api.models.common import Status
from api.models.warehouse import WarehouseTransaction, WhTomasFisicas
from api.serializers.order import OrderSerializer
from api.serializers.purchase import PurchaseSerializer
from api.serializers.warehouse import (
    FullWarehouseSerializer,
    TomasFisicasSerializer,
    WarehouseSerializer,
    WhInventorySerializer,
    WhTransactionSerializer,
    WhWithTomaFisicaSerializer,
)
from api.utils import error_response


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


class WhInventoryView(APIView):
    def get(self, request):

        try:

            wh_inventory = Inventory.objects.filter(
                warehouse__pk=request.query_params.get("id")
            ).order_by("-id")

            page_number = request.query_params.get("page")

            per_page = request.query_params.get("per_page", 15)

            if page_number:

                paginator = Paginator(wh_inventory, per_page)

                page_obj = paginator.get_page(page_number)

                return JsonResponse(
                    {
                        "data": WhInventorySerializer(page_obj, many=True).data,
                        "total": paginator.count,
                        "page": int(page_number),
                        "lastPage": paginator.num_pages,
                    }
                )

            return Response(WhInventorySerializer(wh_inventory, many=True).data)

        except Exception as e:

            return error_response("Invalid query")


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


class WhPurchaseView(APIView):
    def get(self, request):

        try:

            wh_purchases = (
                Purchase.objects.filter(warehouse__pk=request.query_params.get("id"))
                .select_related("invoice")
                .select_related("provider")
                .order_by("-id")
            )

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(
                    wh_purchases, request.query_params.get("per_page", 15)
                )

                page_obj = paginator.get_page(page_number)

                purchase_data = PurchaseSerializer(page_obj, many=True).data

                for purchase in purchase_data:
                    purchase_status = (
                        PurchaseStatus.objects.select_related("status")
                        .filter(purchase__id=purchase.get("id"))
                        .latest("id")
                    )

                    purchase["status"] = purchase_status.status.name

                return JsonResponse(
                    {
                        "data": purchase_data,
                        "total": paginator.count,
                        "page": int(page_number),
                        "lastPage": paginator.num_pages,
                    }
                )

            purchases_data = PurchaseSerializer(wh_purchases, many=True).data

            for purchase in purchases_data:
                purchase_status = (
                    PurchaseStatus.objects.select_related("status")
                    .filter(purchase__id=purchase.get("id"))
                    .latest("id")
                )

                purchase["status"] = purchase_status.status.name

            return JsonResponse(purchases_data, safe=False)

        except Exception as e:
            print(e)
            return error_response("Invalid query")


class WhTransactionView(APIView):
    def get(self, request):
        try:

            wh_transaction_qs = (
                WarehouseTransaction.objects.select_related("status")
                .filter(
                    Q(warehouse_origin__pk=request.query_params.get("id"))
                    | Q(warehouse_destiny__pk=request.query_params.get("id"))
                )
                .order_by("-id")
            )

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(
                    wh_transaction_qs, request.query_params.get("per_page", 15)
                )

                page_obj = paginator.get_page(page_number)

                transactions_data = WhTransactionSerializer(page_obj, many=True).data

                return JsonResponse(
                    {
                        "data": WhTransactionSerializer(page_obj, many=True).data,
                        "total": paginator.count,
                        "page": int(page_number),
                        "lastPage": paginator.num_pages,
                    }
                )

            transactions_data = WhTransactionSerializer(
                wh_transaction_qs, many=True
            ).data

            return JsonResponse(transactions_data, safe=False)

        except Exception as e:
            print(e)
            return error_response("Invalid query")


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


class WhTomaFisicasView(APIView):
    def get(self, request: Request):
        try:
            wh_id = int(request.query_params.get("id"))
            toma_fisica = WhTomasFisicas.objects.filter(warehouse_id=wh_id).order_by(
                "-id"
            )
            if toma_fisica is None:
                return error_response("Not found", status=404)

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(
                    toma_fisica, request.query_params.get("per_page", 15)
                )

                page_obj = paginator.get_page(page_number)

                return JsonResponse(
                    {
                        "data": TomasFisicasSerializer(page_obj, many=True).data,
                        "total": paginator.count,
                        "page": int(page_number),
                        "lastPage": paginator.num_pages,
                    }
                )

            serializer = TomasFisicasSerializer(toma_fisica, many=True)
            return JsonResponse(serializer.data, safe=False)
        except TypeError as e:

            return error_response("invalid params")


class CustomPagination(PageNumberPagination):
    page_size = 15
    page_size_query_param = "per_page"
    page_query_param = "page"


class WhTomaFisicasViewSet(ModelViewSet):

    queryset = Inventory.objects.all()
    serializer_class = WhInventorySerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Inventory.objects.all()
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).prefetch_related("item")

        if params.get("item_name", None):
            queryset = queryset.filter(
                item__name__icontains=params.get("warehouse_name")
            )

        if params.get("min_quantity", None):
            queryset = queryset.filter(quantity__gte=params.get("min_quantity"))

        if params.get("max_quantity", None):
            queryset = queryset.filter(quantity__lte=params.get("max_quantity"))

        if params.get("from_date", None):
            queryset = queryset.filter(updated_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = params.get("to_date", None) + datetime.timedelta(days=1)
            queryset = queryset.filter(updated_at__lte=to_date)

        return queryset
