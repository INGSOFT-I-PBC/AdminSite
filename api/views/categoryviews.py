from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Category
from django.http import JsonResponse
import json
from api.serializers import FullCategorySerializer


class CategoryView(APIView):
    """
    This View holds multiple methods for the Items
    """

    def get(self, request: Request, id=0):
        if id > 0:
            items = Category.objects.filter(id=id)
            serializer = FullCategorySerializer(
                items, context={"request": request}, many=True
            )

            if len(items) > 0:
                datos = Response(serializer.data)

            return datos

        else:
            items = Category.objects.all()
            serializer = FullCategorySerializer(
                items, context={"request": request}, many=True
            )

            if len(items) > 0:
                datos = Response(serializer.data)

            return datos

    def post(self, request: Request):
        pass

    def put(self, request: Request, id):
        pass
