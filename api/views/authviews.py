from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import User, UserPermission, Permission, Group, GroupPermission, WharehouseModel
from api.serializers import UserSerializer, PermissionSerializer


# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class PermissionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retrieves all the permissions that are on the system
    """
    queryset = Permission.objects.all().order_by("codename")
    serializer_class = PermissionSerializer


class WarehouseViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retrieves all the warehouses in the system
    """
    queryset = WharehouseModel.objects.all().order_by("name")

class LogoutViewSet(APIView):
    """
    API endpoint that implement the logout action in the system
    """

    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get("all"):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "goodbye"})
        refresh_token = self.request.data.get("refresh_token")
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})


class PermissionsView(APIView):
    """
    This View returns the permissions of the user
    that use the API.
    """

    def get(self, request, *args, **kwargs):
        user = request.user
        permission_list = []
        try:
            group = GroupPermission.objects.filter(group=user.group)
            for permgroup in group:
                permission_list.append(permgroup.permission.name)
        except ObjectDoesNotExist as ex:
            print("Not found: ", ex)
        return Response(
            {
                "user.name": user.employee.name,
                "user.lastname": user.employee.lastname,
                "user.username": user.username,
                "permissions": permission_list,
            }
        )


@api_view(["POST"])
def reset_password(request: Request):
    data = dict(**request.data)
    user: User = request.user
    try:
        if data["password"] != data["password_confirm"]:
            return JsonResponse(
                {"error": False, "message": "The given password does not match"},
                status=400,
            )
        if len(data["password"]) < 6:
            return JsonResponse(
                {
                    "error": True,
                    "message": "The password need to have a minimum length of 6",
                },
                status=400,
            )
        user.set_password(data["password"])
        user.save()
    except:
        return JsonResponse(
            {"error": True, "message": "Invalid attribute received"},
            status=400,
        )

    return JsonResponse({"error": False, "message": "Ok"})


def user_info():
    pass
