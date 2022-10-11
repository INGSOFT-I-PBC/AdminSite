from unicodedata import name
from api.models.common import Status
from api.models import (
    Warehouse,
    OrderRequest,
    OrderRequestDetail,
    OrderStatus,
    Inventory,
    Item,
)
from api.serializers import WarehouseSerializer, FullWarehouseSerializer
from api.serializers.oders import OrderSerializer, OrderDetailsSerializer

from distutils.log import error
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse

from email import message

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from tkinter import W
from tkinter.tix import Tree

from api.serializers.warehouse import InventorySerializer


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

            inactive_obj = Status.objects.get(name="inactive")

            warehouse_qset = Warehouse.objects.filter(**filters)

            warehouse_qset = warehouse_qset.exclude(status=inactive_obj).latest("id")

            serializer = WarehouseSerializer(warehouse_qset)

            wh_inventory = InventorySerializer(warehouse_qset.inventory_set, many=True)

            return JsonResponse(
                {"warehouse": serializer.data, "inventory": wh_inventory.data}
            )

        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )

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
            print(e)
            return JsonResponse(
                {"error": True, "message": "Object not found"},
                status=400,
            )

    def post(self, request: Request):

        data = dict(**request.data)

        try:

            valid_status = Status.objects.get(name="active")

            data["status"] = valid_status.id

            serializer = WarehouseSerializer(data=data)

            serializer.is_valid(raise_exception=True)

            serializer.update()

        except Exception as e:

            return JsonResponse(
                {"error": True, "message": "Invalid attributes received"},
                status=400,
            )

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

            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )


class WarehouseViewSet(ReadOnlyModelViewSet):

    queryset = (
        Warehouse.objects.all()
        .order_by("name")
        .exclude(status__name="inactive")
        .order_by("name")
    )
    serializer_class = FullWarehouseSerializer


class FullWarehouseViewSet(WarehouseViewSet):
    pagination_class = None


class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = WarehouseSerializer(queryset, many=True)

    def list(self, request):

        page_number = request.query_params.get("page")

        if page_number:

            paginator = Paginator(self.queryset, 50)

            page_obj = paginator.get_page(page_number)

            return Response(OrderSerializer(page_obj, many=True).data)

        return Response(self.serializer_class.data)


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

            return Response(OrderSerializer(wh_orders, many=True))

        except:
            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )

    def post(self):

        pass

    def put(self):
        pass

    def delete(self):
        pass


class WhOrderRequestViewSet(ReadOnlyModelViewSet):
    """
    API Endpoint that allows only read operation on the given Orders that are registered and available
    """

    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = OrderSerializer(queryset, many=True)
