from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet

from api.models import OrderRequest
from api.serializers.order import (
    OrderDetailSerializer,
    OrderReadSerializer,
    OrderSerializer,
    PartialOrderSerializer,
)
from api.utils import error_response, response


class OrderRequestViewSet(ReadOnlyModelViewSet):
    queryset = OrderRequest.objects.all().order_by("-requested_at")
    serializer_class = OrderReadSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()
        if params.get("comment", None):
            queryset = queryset.filter(comment__icontains=params.get("comment"))

        return queryset


class OrderRequestView(APIView):
    def get(self, request: Request, id):
        query = OrderRequest.objects.filter(pk=id)
        if not query.exists():
            return error_response(
                "The requested Order Request was not found", status=404
            )

        return JsonResponse(OrderSerializer(query.get()).data)

    def patch(self, request: Request, id):
        query = OrderRequest.objects.filter(id=id)
        if not query.exists():
            return error_response("The target order request doesn't exists", status=404)
        target = query.get()
        if target.status in ("AP", "NG"):
            return error_response(
                "The order request has been revised already", code="ERR_REVISED"
            )
        new_data = request.data
        new_status = new_data.get("status", None)
        serialized = PartialOrderSerializer(target, data=new_data)
        serialized.is_valid(raise_exception=True)
        target = serialized.save()
        if new_status in ("AP", "NG"):
            target.revised_at = datetime.now()
            target.revised_by = request.user.employee
            target.save()
        return response("Successfully updated order request")


@api_view(["POST"])
def create_order_request(request):
    if not request.data:
        return error_response("No data was provided")
    items = request.data.pop("items")
    items = [x for x in items if x]
    if not items:
        return error_response("An order need at least one item")

    data = request.data
    data["requested_by"] = request.user.employee_id
    serializer = OrderSerializer(data=data)

    if serializer.is_valid(raise_exception=True):
        order: OrderRequest = serializer.save()
        for item in items:
            # inject order, due client doesn't know which is created
            item["order_request"] = order.pk
        item_serializer = OrderDetailSerializer(data=items, many=True)
        try:  # Check if the inserted items are valid
            item_serializer.is_valid(raise_exception=True)
        except Exception as e:
            order.delete()
            raise e
        item_serializer.save()
        serializer = OrderSerializer(order)
        return JsonResponse(serializer.data, status=201)
    return error_response("The given data was invalid")


@api_view(["GET"])
def get_full_order(request, *args, **kwargs):
    search = OrderRequest.objects.filter(**kwargs)
    if not search.exists():
        return error_response("The given order was not found", status=404)
    order = search.get()

    return JsonResponse(OrderReadSerializer(order).data)
