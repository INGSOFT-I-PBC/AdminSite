from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Category, Item
from django.http import JsonResponse
import json
from api.serializers import FullItemSerializer


class ItemView(APIView):
    """
    This View holds multiple methods for the Items
    """

    def get(self, request: Request, id=0):
        if id > 0:
            items = Item.objects.filter(id=id)
            serializer = FullItemSerializer(
                items, context={"request": request}, many=True
            )

            if len(items) > 0:
                datos = Response(serializer.data)

            return datos

        else:
            items = list(Item.objects.values())
            if len(items) > 0:
                datos = {"message": "Success", "items": items}
            else:
                datos = {"message": "Items not found .."}
            return JsonResponse(datos)

    def post(self, request: Request):
        jd = json.loads(request.body)
        Item.objects.create(
            created_at=jd["created_at"],
            updated_at=jd["updated_at"],
            deleted_at=jd["deleted_at"],
            brand=jd["brand"],
            category_id=jd["category_id"],
            created_by_id=jd["created_by_id"],
            img=jd["img"],
            iva=jd["iva"],
            model=jd["model"],
            name=jd["name"],
            price=jd["price"],
            status_id=jd["status_id"],
        )
        datos = {"message": "Success"}
        return JsonResponse(datos)

    def put(self, request: Request, id):
        jd = json.loads(request.body)
        items = list(Item.objects.filter(id=id).values())
        if len(items) > 0:
            item = Item.objects.get(id=id)
            item.created_at = jd["created_at"]
            item.updated_at = jd["updated_at"]
            item.deleted_at = jd["deleted_at"]
            item.brand = jd["brand"]
            item.category_id = jd["category_id"]
            item.created_by_id = jd["created_by_id"]
            item.img = jd["img"]
            item.iva = jd["iva"]
            item.model = jd["model"]
            item.name = jd["name"]
            item.price = jd["price"]
            item.status_id = jd["status_id"]
            item.save()
            datos = {"message": "Success"}

        else:
            datos = {"message": "Items not found .."}

        return JsonResponse(datos)

    def delete(self, request: Request, id):
        """
        This method would deactivate a items.
        Args:
            request: The Request

        Returns:
            A response with the status information about the action
            executed.

        """
        items = list(Item.objects.filter(id=id).values())
        if len(items) > 0:
            Item.objects.filter(id=id).delete()
            datos = {"message": "Success"}

        else:
            datos = {"message": "Items not found .."}

        return JsonResponse(datos)
