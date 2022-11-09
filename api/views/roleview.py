from django.contrib.auth.hashers import make_password
from django.db.models import Model
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView

from api.models import Role
from api.serializers.auth import *
from api.serializers.role import RoleSerializer, UpdateRoleSerializer
from api.utils import error_response, response
from rest_framework import viewsets

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
        role = Role.objects.get(**kwargs)
        updated_model = UpdateRoleSerializer(role, data=request.data)
        updated_model.is_valid(raise_exception=True)
        updated_model.save()
        return response("The role was updated successfully")


class RoleViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allow the preview of employees
    """
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
