from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Inventory, Item
from django.http import JsonResponse
import json
from api.serializers import FullInventorySerializer, InventorySerializer
from rest_framework import serializers
from rest_framework import status


class InventoryView(APIView):
    """
    This View holds multiple methods for the Items
    """

    def get(self, request: Request, id=0):
        if id > 0:
            items = Inventory.objects.filter(id=id)
            serializer = FullInventorySerializer(
                items, context={"request": request}, many=True
            )

            if len(items) > 0:
                datos = Response(serializer.data)

            return datos

        else:
            items = Inventory.objects.all().order_by("id")
            serializer = FullInventorySerializer(
                items, context={"request": request}, many=True
            )
            if len(items) > 0:
                datos = Response(serializer.data)
                print(datos)

            return datos

    def post(self, request: Request):
        jd = json.loads(request.body)
        Inventory.objects.create(
            created_at=jd["created_at"],
            updated_at=jd["updated_at"],
            deleted_at=jd["deleted_at"],
            quantity=jd["quantity"],
            item_id=jd["item_id"],
            updated_by_id=jd["updated_by_id"],
            warehouse_id=jd["warehouse_id"],
        )
        datos = {"message": "Success"}
        return JsonResponse(datos)

    def put(self, request: Request, id):
        pass

    def delete(self, request: Request, id):
        pass
