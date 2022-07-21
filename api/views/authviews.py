from api.models import User, UserPermission

# from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import UserSerializer
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by("id")
    serializer_class = UserSerializer


class LogoutView(APIView):
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
            permissions = UserPermission.objects.filter(user=user.id)
            for permission in permissions:
                permission_list.append(
                    {"name": permission.permission.name, "id": permission.permission.codename}
                )
        except ObjectDoesNotExist as ex:
            print("Not found: ", ex)
        return Response(
            {
                "user.name": user.name,
                "user.lastname": user.lastname,
                "user.username": user.username,
                "permissions": permission_list,
            }
        )


def user_info():
    pass
