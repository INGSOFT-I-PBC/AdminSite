from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import Role
from api.serializers.auth import *
from api.serializers.role import RoleSerializer
from api.utils import error_response, response


class RoleView(APIView):
    """
    This class handle the request with a single element of the
    Role model.
    """

    def get(self, request: Request, *args, **kwargs):
        if not Role.objects.filter(**kwargs).exists():
            return error_response("the given role doesn't exists")
        role = Role.objects.get(**kwargs)
        return JsonResponse(data=RoleSerializer(role).data)

    def put(self, request: Request, *args, **kwargs):
        if not Role.objects.filter(**kwargs).exists():
            return error_response("The given role doesn't exists")
        if not request.data:
            return error_response("No data provided")

        name = request.data.get("name", None)
        codename = request.data.get("codename", None)
        id = request.data.get("id", None)

        # Now if name and codename is provided, check the two cases
        if name and codename:
            # If role already exists(if needed or send error)
            if (
                Role.objects.filter(name=name).exclude(id=id).exists()
                or Role.objects.filter(codename=codename).exclude(id=id).exists()
            ):
                return error_response("The role already exists")

            # else:  # Create a new role
            role = Role.objects.get(**kwargs)
            updated_role = RoleSerializer(role, data=request.data)
            updated_role.is_valid(raise_exception=True)
            updated_role.save()
            return JsonResponse(RoleSerializer(role).data)
        return response("The role wasn't updated")

    def delete(self, request: Request, *args, **kwargs):
        if not Role.objects.filter(**kwargs).exists():
            return error_response("The given role doesn't exists")
        role = Role.objects.get(**kwargs)
        role.delete()
        return response("Role deleted successfully")


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allow the preview of employees
    """

    queryset = Role.objects.all().order_by("-id")
    serializer_class = RoleSerializer


"""
    API endpoint that allow the create a role
"""


@api_view(["POST"])
def create_role(request: Request, *args, **kwargs):
    if not request.data:
        return error_response("No data was provided")
    if not request.data:
        return error_response("No data was provided")

    name = request.data.get("name", None)
    codename = request.data.get("codename", None)
    # Now if name and codename is provided, check the two cases
    if name and codename:
        # If role already exists(if needed or send error)
        if (
            Role.objects.filter(name=name).exists()
            or Role.objects.filter(codename=codename).exists()
        ):
            return error_response("Rol existente")
        # else:  # Create a new role
        role = RoleSerializer(data=request.data)
        role.is_valid(raise_exception=True)
        role = role.save()
        return JsonResponse(RoleSerializer(role).data)
    return error_response("No name and codename was provided")
