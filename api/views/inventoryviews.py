import datetime

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import Employee, Inventory, Item, Warehouse
from api.serializers import FullInventorySerializer, InventorySerializer
from api.serializers.warehouse import WhInventorySerializer


class InventoryView(APIView):
    """
    This View holds multiple methods for the Inventory
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
            items = Inventory.objects.all().order_by("-created_at")
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

    def put(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        save_allowance = get_object_or_404(Inventory.objects.all(), pk=pk)
        serializer = InventorySerializer(save_allowance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

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


class FullInventoryViewSet(ReadOnlyModelViewSet):

    queryset = Inventory.objects.all().order_by("-created_at")
    serializer_class = FullInventorySerializer
class FullInventoryViewSet2(ModelViewSet):

    queryset = Inventory.objects.all().order_by("-created_at")
    serializer_class = FullInventorySerializer
    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("id", None):
            queryset = queryset.filter(id=params.get("id", None))
            return queryset

        if params.get("code", None):
            queryset = queryset.filter(item__codename__icontains=params.get("code"))

        if params.get("stock", None):
            queryset = queryset.filter(quantity__gte = params.get("stock"))

        if params.get("name", None):
            queryset = queryset.filter(item__name__icontains=params.get("name"))

        if params.get("category", None):
            queryset = queryset.filter(item__category__name__icontains=params.get("category"))


        return queryset




class InventoryViewSet(ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """

    queryset = Inventory.objects.all()
    serializer_class = WhInventorySerializer

    def get_queryset(self):
        queryset = Inventory.objects.all()
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).prefetch_related("item")

        if params.get("item_name", None):
            queryset = queryset.filter(
                item__name__icontains=params.get("warehouse_name")
            )

        if params.get("min_quantity", None):
            queryset = queryset.filter(quantity__gte=params.get("min_quantity"))

        if params.get("max_quantity", None):
            queryset = queryset.filter(quantity__lte=params.get("max_quantity"))

        if params.get("from_date", None):
            queryset = queryset.filter(updated_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = params.get("to_date", None) + datetime.timedelta(days=1)
            queryset = queryset.filter(updated_at__lte=to_date)

        return queryset
