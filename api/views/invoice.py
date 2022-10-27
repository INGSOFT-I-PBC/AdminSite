from unicodedata import name
from api.models.common import Status
from api.models import (
    Warehouse,
    OrderRequest,
    Purchase,
    Invoice,
    PurchaseStatus,
    warehouse,
)
from api.serializers.warehouse import (
    WarehouseSerializer,
    FullWarehouseSerializer,
)
from api.serializers.order import OrderSerializer

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.utils import error_response
from api.serializers.invoice import InvoiceSerializer


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


class   InvoiceView(APIView):
    def get(self, request):

        try:
            wh_inventory = Invoice.objects.all().order_by("id")
            """wh_inventory = Invoice.objects.filter(
                client__pk=request.query_params.get("id")
            ).order_by("-id")"""
            print("hola")
            print(wh_inventory)

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(wh_inventory, 5)

                page_obj = paginator.get_page(page_number)

                return Response(InvoiceSerializer(page_obj, many=True).data)

            return Response(InvoiceSerializer(wh_inventory, many=True).data)

        except Exception as e:
            print(e)
            return error_response("Invalid query")


class WhOrderRequestView(APIView):
    def get(self, request):

        try:

            wh_orders = OrderRequest.objects.filter(
                warehouse__pk=request.query_params.get("id")
            ).order_by("-id")

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(wh_orders, 50)

                page_obj = paginator.get_page(page_number)

                return Response(OrderSerializer(page_obj, many=True).data)

            return Response(OrderSerializer(wh_orders, many=True).data)

        except:
            return error_response("Invalid query")


class WhPurchaseView(APIView):
    def get(self, request):
        try:

            wh_purchases = Purchase.objects.filter(
                warehouse__pk=request.query_params.get("id")
            ).order_by("-id")

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(wh_purchases, 50)

                page_obj = paginator.get_page(page_number)

                purchase_data = PurchaseSerializer(page_obj, many=True).data

                for purchase in purchase_data:
                    purchase_status = (
                        PurchaseStatus.objects.select_related("status")
                        .filter(purchase__id=purchase.get("id"))
                        .latest("id")
                    )

                    purchase["status"] = purchase_status.status.name

                return JsonResponse(purchase_data, safe=False)

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

            return error_response("Invalid query")


class WhTransactionView(APIView):
    def get(self, request):
        try:

            wh_transaction_qs = (
                warehouse.WarehouseTransaction.objects.select_related("status")
                .filter(
                    Q(warehouse_origin__pk=request.query_params.get("id"))
                    | Q(warehouse_destiny__pk=request.query_params.get("id"))
                )
                .order_by("-id")
            )

            page_number = request.query_params.get("page")

            if page_number:

                paginator = Paginator(wh_transaction_qs, 50)

                page_obj = paginator.get_page(page_number)

                transactions_data = WhTransactionSerializer(page_obj, many=True).data

                return JsonResponse(transactions_data, safe=False)

            transactions_data = WhTransactionSerializer(
                wh_transaction_qs, many=True
            ).data

            return JsonResponse(transactions_data)

        except Exception as e:
            print(e)
            return error_response("Invalid query")


class WhOrderRequestViewSet(ReadOnlyModelViewSet):
    """
    API Endpoint that allows only read operation on the given Orders that are registered and available
    """

    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = OrderSerializer(queryset, many=True)
