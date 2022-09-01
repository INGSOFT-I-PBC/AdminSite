from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView


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
