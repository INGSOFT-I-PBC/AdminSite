from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_framework import viewsets, status
from api.models import  Gender
from api.serializers import GenderSerializer
from rest_framework.permissions import IsAuthenticated
from api.utils import error_response
from django.http import JsonResponse


class GenderView(ReadOnlyModelViewSet):
    queryset = Gender.objects.all().order_by("name")
    serializer_class = GenderSerializer

class FullGenderViewSet(GenderView):
    pagination_class = None

