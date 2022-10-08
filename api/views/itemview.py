from webbrowser import get
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import viewsets, status
from api.models import Item
from api.serializers import ItemSerializer
from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response


class ItemView(APIView):
    def get(self, request: Request, id: int):
        pass

    def delete(self, request: Request, id: int):
        pass

    def put(self, request: Request, id: int, data):
        pass


class PaginatedItemViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    # def list(self, request):
    #     items = Item.objects.all()

    # @detail_route()
    # def all(self, request):
    #     pass


class ItemViewSet(viewsets.ViewSet):
    pagination_class = None

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)
