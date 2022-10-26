from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Province,City
from api.serializers import ProvinceSerializer
from api.utils import error_response
from django.http import JsonResponse


class ProvinceViewSet(ReadOnlyModelViewSet):
    queryset = Province.objects.all().order_by("name")
    serializer_class = ProvinceSerializer

class FullProvinceViewSet(ProvinceViewSet):
    pagination_class = None

class ProvinceCityView(APIView):
    def get(self, request):

        try:

            province_city = City.objects.filter(
                province__pk=request.query_params.get("id")
            ).order_by("-id")

            return Response(ProvinceSerializer(province_city, many=True).data)

        except Exception as e:
            print(e)
            return JsonResponse(
                {"error": True, "message": "Invalid query"},
                status=400,
            )


'''class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("id")
    serializer_class = ClientSerializer'''



