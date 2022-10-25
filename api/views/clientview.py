from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import  Client
from api.serializers import ClientSerializer, FullClientSerializer


class ClientView(APIView):
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


class ClientViewSet(ReadOnlyModelViewSet):
    queryset = Client.objects.all().order_by("name")
    serializer_class = FullClientSerializer


class FullClientViewSet(ClientViewSet):
    pagination_class = None


'''class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = ClientSerializer'''


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
