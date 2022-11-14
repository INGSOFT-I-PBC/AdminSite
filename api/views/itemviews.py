from api import serializers
from api.serializers.items import ItemSerializer, ItemSerializer2
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from api.models import Category, Item, Status
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
import json
from api.serializers import FullItemSerializer
from api.forms import UploadForm
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from django.db.models.signals import pre_delete
from django.dispatch.dispatcher import receiver


class ItemView(APIView):
    """
    This View holds multiple methods for the Items
    """

    # authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    parser_classes = (JSONParser, FormParser, MultiPartParser)

    def get(self, request: Request, *args, **kwargs):
        pk = self.kwargs.get("pk")

        if pk != None:
            if pk > 0:

                items = Item.objects.filter(id=pk)


                serializer = FullItemSerializer(
                    items, context={"request": request}, many=True
                )

                if len(list(items)) > 0:
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

        serializer = ItemSerializer(data=request.data)  # type: ignore
        cateid = self.request.data.get("category_id") # type: ignore
        staid = self.request.data.get("status_id")# type: ignore

        if serializer.is_valid():
            serializer.save(
                category=Category.objects.get(pk=cateid),
                status=Status.objects.get(pk=staid),
            )
            return Response(serializer.data, status=200)
        else:
            return Response(serializer.errors, status=400)

    # Workshop_Pivotal_Tracker__SCM_03_W5Gtr9V.jpg
    def put(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        save_allowance = get_object_or_404(Item.objects.all(), pk=pk)
        serializer = ItemSerializer2(save_allowance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data)
        return JsonResponse(serializer.errors, status=400)

    def delete(self, request: Request, *args, **kwargs):
        """
        This method would deactivate a items.
        Args:
            request: The Request

        Returns:
            A response with the status information about the action
            executed.

        """
        pk = self.kwargs.get("pk")
        items = Item.objects.filter(id=pk)
        # items = list(Item.objects.filter(id=id).values())
        if len(list(items)) > 0:
            items.delete()
            datos = {"message": "Success"}

        else:
            datos = {"message": "Items not found .."}

        return JsonResponse(datos)

    @receiver(pre_delete, sender=Item)
    def mymodel_delete(sender, instance, **kwargs):
        # Pass false so FileField doesn't save the model.
        instance.img.delete(False)
