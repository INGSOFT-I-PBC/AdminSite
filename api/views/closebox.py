from datetime import datetime

# from django.shortcuts import render
from django.db.models import Sum
from django.http import JsonResponse
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import (
    Employee,
    Group,
    GroupPermission,
    Inventory,
    Permission,
    Role,
    User,
)
from api.serializers import (
    GroupSerializer,
    PermissionSerializer,
    ShowEmployeeSerializer,
    UserSerializer,
)
from api.utils import bool_param, error_response, response


class CloseBoxViewDataInventory(ModelViewSet):

    queryset = Inventory.objects.filter(payment_method_id=1).aggregate(Sum("total"))[
        "column__sum"
    ]
