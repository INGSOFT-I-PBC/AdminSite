from email import message
from operator import truediv
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api import serializers


from api.models.common import Status
from api.models import Warehouse, OrderRequest
from api.serializers import WarehouseSerializer, FullWarehouseSerializer
from django.http import JsonResponse


class WarehouseView(APIView):
    """
    This View holds multiple methods for the Warehouse
    """

    def get(self, request: Request):

        try:
            querydict = request.query_params
            warehouse = Warehouse.objects.get(pk=querydict["id"])
            status = warehouse.status.name

            if status == "invalid":
                return JsonResponse(
                    {"error": True, "message": "Warehouse invalid"},
                    status=400,
                )

            serializer_class = WarehouseSerializer(warehouse)
            return Response(serializer_class.data)

        except:

            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )

    def post(self, request: Request):

        data = dict(**request.data)

        try:

            valid_status = Status.objects.get(name="active")

            data["status"] = valid_status.id

            serializer = WarehouseSerializer(data=data)

            serializer.is_valid(raise_exception=True)

            serializer.save()

        except:
            return JsonResponse(
                {"error": True, "message": "Invalid attribute received"},
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

        return Response({})


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
