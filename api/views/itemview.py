from django.http import JsonResponse
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Item, ItemMetaData
from api.serializers import ItemSerializer, FullItemSerializer


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


class ItemViewSet(viewsets.ViewSet):
    pagination_class = None

    def list(self, request):
        queryset = Item.objects.all()
        serializer = ItemSerializer(queryset, many=True)
        return Response(serializer.data)


@api_view(["GET"])
def find_item(request, id: int):
    item = Item.objects.filter(pk=id).first()
    if item is None:
        return JsonResponse(
            {"error": True, "message": "Item not found", "code": "NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = FullItemSerializer(item)
    return JsonResponse(serializer.data)


@api_view(["GET"])
def get_item_properties(request, id: int):
    item = Item.objects.filter(pk=id).first()
    if item is None:
        return JsonResponse(
            {"error": True, "message": "Item not found", "code": "NOT_FOUND"},
            status=status.HTTP_404_NOT_FOUND,
        )
    props = ItemMetaData.objects.filter(item=item)
    out = []
    for prop in props:
        fallback = prop.param.default_value
        out.append(
            {
                "name": prop.param.field,
                "type": prop.param.field_type,
                "value": fallback if prop.value is None else prop.value,
            }
        )
    return JsonResponse(out, safe=False)
