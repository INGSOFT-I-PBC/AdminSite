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
        active_status = Status.objects.get(name="active").id
        provider = Provider.objects.filter(**kwargs, status=active_status)
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

        return response("provider updated successfully")

    def delete(self, request: Request, *args, **kwargs):
        active_status = Status.objects.get(name="active").id
        provider = Provider.objects.filter(**kwargs, status=active_status)
        if not provider.exists():
            return error_response(
                "The requested provider doesn't exists", "ERR_NOT_EXISTS"
            )
        target = provider.first()
        target.deleted_by = request.user.employee
        target.deleted_at = datetime.now()
        target.status = Status.objects.get(name="inactive")
        target.save()
        post_data = ProviderSerializer(target)

        return JsonResponse(post_data.data)


@api_view(["POST"])
def create_provider(request: Request):
    data = request.data
    if not data:
        return error_response("No data was provided")

    data["created_by"] = request.user.id
    data["status"] = Status.objects.get(name="active").id
    provider_data = ProviderSerializer(data=data)
    search = Provider.objects.filter(
        status=Status.objects.get(name="inactive"), document_path=data["document_path"]
    )
    if search.exists():
        provider_data = ProviderSerializer(search.first(), data=data)
    provider_data.is_valid(raise_exception=True)
    provider_data.save()
    return JsonResponse(data=provider_data.data)
