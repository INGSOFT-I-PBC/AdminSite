from webbrowser import get
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework import viewsets, status
from api.models import Item


class ItemView(APIView):
    def get(self, request: Request, id: int):
        pass

    def delete(self, request: Request, id: int):
        pass

    def put(self, request: Request, id: int, data):
        pass


class ItemViewSet(viewsets.ViewSet):
    def list(self, request):
        queryset = Item.objects.all()
