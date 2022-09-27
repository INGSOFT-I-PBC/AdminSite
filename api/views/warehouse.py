from distutils.log import error
from email import message

from operator import truediv, and_
from tkinter import W
from tkinter.tix import Tree
from django.db.models import Q
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api import serializers


from api.models.common import Status
from api.models import Warehouse, OrderRequest, warehouse
from api.serializers import WarehouseSerializer, FullWarehouseSerializer
from django.http import JsonResponse


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

            filters["status"] = Status.objects.get(name="active")

            warehouse_qset = Warehouse.objects.filter(**filters)

            serializer = WarehouseSerializer(warehouse_qset, many=True)

            return Response(serializer.data)

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
            print(e)
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
            print(e)
            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )


class WarehouseViewSet(ReadOnlyModelViewSet):
    queryset = Warehouse.objects.all().order_by("name")
    serializer_class = FullWarehouseSerializer(queryset, many=True)

    def list(self, request):
        queryset = Warehouse.objects.all().order_by("name")
        serializer_class = FullWarehouseSerializer(queryset, many=True)
        return Response(serializer_class.data)


class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = WarehouseSerializer


class WhOrderRequestView(APIView):
    def get(self):
        pass

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
