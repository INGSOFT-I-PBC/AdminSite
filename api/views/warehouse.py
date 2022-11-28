from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import Warehouse
from api.models.warehouse import WarehouseBarcode
from api.serializers import FullWarehouseSerializer
from api.serializers.warehouse import ROBarcodeSerializer, WhBarcodeSerializer
from api.utils import error_response, response


class WarehouseView(APIView):
    """
    This View holds multiple methods for the Warehouse
    """

    def get(self, request: Request):
        return Response({})

    def post(self, request: Request):
        return Response({})

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
    serializer_class = FullWarehouseSerializer


class FullWarehouseViewSet(WarehouseViewSet):
    pagination_class = None


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


class BarcodeView(APIView):
    def get(self, request: Request, *args, **kwargs):
        search = WarehouseBarcode.objects.filter(**kwargs)

        if not search.exists():
            return error_response("The requested barcode doesn't exists", status=404)

        result = search.get()

        return JsonResponse(ROBarcodeSerializer(result).data)

    def put(self, request: Request):
        pass  # TODO: Create this endpoint

    def patch(self, request: Request):
        pass  # TODO: Create this endpoint


@api_view(["POST"])
def create_stock_barcode(request: Request):
    data = request.data
    if not data:
        return error_response("No data provided to save", status=401)

    serialized = WhBarcodeSerializer(data=data)
    serialized.is_valid(raise_exception=True)
    serialized.save()
    return response("Saved correctly", status=201)
