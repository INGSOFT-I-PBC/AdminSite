from datetime import datetime

from django.http import JsonResponse

# from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)
from rest_framework_simplejwt.tokens import RefreshToken

from api.models import Employee, Group, GroupPermission, Permission, Role, User
from api.serializers import (
    GroupSerializer,
    PermissionSerializer,
    ShowEmployeeSerializer,
    UserSerializer,
)
from api.utils import bool_param, error_response, response


class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """

    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()

        status = params.pop(
            "active",
            [None],
        )[0]
        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)
        if status is not None:
            queryset = queryset.filter(is_active=bool_param(status))
        if params.get("username", None):
            queryset = queryset.filter(username__icontains=params.get("username"))
        if params.get("email", None):
            queryset = queryset.filter(email__icontains=params.get("email"))
        if params.get("is_active", None):
            queryset = queryset.filter(is_active=bool(params.get("is_active", False)))
        if params.get("group", None):
            queryset = queryset.filter(group=params.get("group"))
        if params.get("role", None):
            queryset = queryset.filter(employee__role=params.get("role"))

        return queryset


class EmployeeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allow the preview of employees
    """

    queryset = Employee.objects.all().order_by("-id")
    serializer_class = ShowEmployeeSerializer


class PermissionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint that retrieves all the permissions that are on the system
    """

    queryset = Permission.objects.all().order_by("codename")
    serializer_class = PermissionSerializer


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
            return Response({"message": "goodbye"})
        refresh_token = self.request.data.get("refresh_token")
        if not refresh_token:
            return JsonResponse(
                {"message": "You cannot logout, 'refresh_token' field is required"},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"message": "OK, goodbye"})


class PermissionsView(APIView):
    """
    This View returns the permissions of the user
    that use the API.
    """

    def get(self, request, *args, **kwargs):
        perms = Permission.objects.filter(**kwargs)
        if not perms.exists():
            return error_response("No permission was found")
        return JsonResponse(data=PermissionSerializer(perms.first()).data)

    def put(self, request: Request, *args, **kwargs):
        perms = Permission.objects.filter(**kwargs)
        if not perms.exists():
            return error_response("No permission was found")
        new_data = PermissionSerializer(perms.first(), request.data)
        new_data.is_valid(raise_exception=True)
        new_data.save()
        return response("permission updated successfully")


class PermissionGroupView(APIView):
    def get(self, request, *args, **kwargs):
        group = Group.objects.get(**kwargs)
        serializer = GroupSerializer(group)
        return JsonResponse(serializer.data)


@api_view(["GET"])
def user_data(request: Request):
    user: User = request.user
    role: Role = user.employee.role
    gperms = GroupPermission.objects.filter(group=user.group)
    permissions = []
    for gperm in gperms:
        permissions.append(gperm.permission.name)
    return JsonResponse(
        {
            "employee": user.employee.id,
            "name": user.employee.name,
            "username": user.username,
            "role": role.name,
            "permissions": permissions,
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
        user.updated_at = datetime.now()
        user.save()
    except:
        return JsonResponse(
            {"error": True, "message": "Invalid attribute received"},
            status=400,
        )

    return JsonResponse({"error": False, "message": "Ok"})


@api_view(["GET"])
def self_permissions():
    user = request.user
    permission_list = []

    group = GroupPermission.objects.filter(group=user.group)
    for permgroup in group:
        permission_list.append(permgroup.permission.name)

    return Response(
        {
            "user.name": user.employee.name,
            "user.lastname": user.employee.lastname,
            "user.username": user.username,
            "permissions": permission_list,
        }
    )


@api_view(["POST"])
def create_permission(request: Request, *args, **kwargs):
    new_permission = PermissionSerializer(data=request.data)
    new_permission.is_valid(raise_exception=True)
    if Permission.objects.filter(codename=request.data["codename"]).exists():
        return error_response("The given permission already exists")
    new_permission.save()
    return response("Permission created successfully")
