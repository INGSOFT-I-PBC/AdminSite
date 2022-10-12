from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Inventory, Item
from django.http import JsonResponse
import json
from api.models import Warehouse, Item, Employee
from api.serializers import FullInventorySerializer, InventorySerializer
from rest_framework import serializers
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated


class InventoryView(APIView):
    """
    This View holds multiple methods for the Items
    """

    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        if pk != None:
            if pk > 0:
                items = Inventory.objects.filter(id=pk)
                serializer = FullInventorySerializer(
                    items, context={"request": request}, many=True
                )

                if len(list(items)) > 0:
                    datos2 = Response(serializer.data)

                return datos2

        else:
            items = Inventory.objects.all().order_by("id")
            serializer = FullInventorySerializer(
                items, context={"request": request}, many=True
            )

            if len(list(items)) > 0:
                datos1 = Response(serializer.data)

            else:
                datos1 = JsonResponse({"message": "Items not found .."})

            return datos1

    def post(self, request: Request):
        serializer = InventorySerializer(data=request.data)
        wareid = self.request.data.get("warehouse_id")
        itemid = self.request.data.get("item_id")
        updateid = self.request.data.get("updated_by_id")

        if serializer.is_valid():
            serializer.save(
                warehouse=Warehouse.objects.get(pk=wareid),
                item=Item.objects.get(pk=itemid),
                updated_by=Employee.objects.get(pk=updateid),
            )
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request: Request, id):
        pass

    def delete(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        inventory = Inventory.objects.filter(id=pk)
        # items = list(Item.objects.filter(id=id).values())
        if len(list(inventory)) > 0:
            inventory.delete()
            datos3 = {"message": "Success"}

        else:
            datos3 = {"message": "Items not found .."}

        return JsonResponse(datos3)
