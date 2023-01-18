from datetime import datetime

from django.http import JsonResponse
from rest_framework import views, viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request

from api.models import Provider
from api.models.common import Status
from api.serializers.provider import PartialProviderSerializer, ProviderSerializer
from api.utils import error_response, response


class ProviderViewSet(viewsets.ReadOnlyModelViewSet):
    """Provider View set
    This view set provides only a read only list to preview the providers
    registered on the system

    Args:
        viewsets (rest_framework.viewsets.ReadOnlyModelViewSet): The superclass for RO Viewsets
    """

    queryset = Provider.objects.order_by("name", "document_path")
    serializer_class = ProviderSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()
        if params.get("name", None):
            queryset = queryset.filter(name__icontains=params.get("name"))
        if params.get("bussiness_name", None):
            queryset = queryset.filter(name__icontains=params.get("bussines_name"))
        if params.get("email", None):
            queryset = queryset.filter(email__icontains=params.get("email"))
        if params.get("document_path", None):
            queryset = queryset.filter(
                document_path__icontains=params.get("document_path")
            )
        return queryset

    class Meta:
        model = Provider


class ProviderView(views.APIView):
    def get(self, request: Request, *args, **kwargs):
        provider = Provider.objects.filter(**kwargs)
        if not provider.exists():
            return error_response(
                "The requested provider doesn't exists", "ERR_NOT_EXISTS"
            )
        return JsonResponse(ProviderSerializer(provider.first()).data)

    def put(self, request: Request, **kwargs):
        provider = Provider.objects.filter(**kwargs, is_active=True)
        if not provider.exists():
            return error_response(
                "The requested provider doesn't exists", "ERR_NOT_EXISTS"
            )
        data = request.data
        if not data:
            return error_response("No data was provided to update")
        target = provider.first()
        new_data = PartialProviderSerializer(target, data=data)
        new_data.is_valid(raise_exception=True)
        new_data.save()

        return response("provider updated successfully", code="UPD_SUCCESS")

    def delete(self, request: Request, *args, **kwargs):
        provider = Provider.objects.filter(**kwargs, is_active=True)
        if not provider.exists():
            return error_response(
                "The requested provider doesn't exists", "ERR_NOT_EXISTS"
            )
        target = provider.first()
        target.delete()

        return response("Provider deactivated succesfully", code="PROV_DEACTIVATED")


@api_view(["POST"])
def create_provider(request: Request):
    data = request.data
    if not data:
        return error_response("No data was provided")
    provider_data = ProviderSerializer(data=data)
    search = Provider.objects.filter(
        document_path=data["document_path"]
    )
    if search.exists() and search.first().is_active:
        return error_response("The given provider already exists")
    if search.exists():
        target = search.first()
        target.is_active = True
        target.save()
        return JsonResponse(data=ProviderSerializer(target).data)

    provider_data.is_valid(raise_exception=True)
    provider_data.save()
    return JsonResponse(data=provider_data.data)
