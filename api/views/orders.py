from datetime import datetime

from django.db.models import Q
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import OrderRequest
from api.models.common import Status
from api.models.orders import OrderRequestDetail, OrderStatus
from api.serializers.order import (
    CreateOrderStatusSerializer,
    FullOrderDetailSerializer,
    OrderDetailSerializer,
    OrderReadSerializer,
    OrderSerializer,
    OrderStatusSerializer,
    PartialOrderSerializer,
    SimplifiedOrderSerializer,
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

    class Meta:

        model = OrderRequest


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


class OrderRequestDetailFullView(ModelViewSet):
    queryset = OrderRequestDetail.objects.all().order_by("id")
    serializer_class = FullOrderDetailSerializer
    pagination_class = None

    def get_queryset(self):
        params = self.request.query_params
        queryset = self.queryset.select_related("item").select_related("item__product")

        if params.get("order_id", None):
            queryset = queryset.filter(order_request=params.get("order_id"))

        if params.get("item_name"):
            queryset = queryset.filter(
                Q(item__product__name__icontains=params.get("name")) |
                Q(item__name__icontains=params.get("name")))

        return queryset


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


@api_view(["PUT"])
def reject_order(request):
    if not request.data:
        return error_response("No data was provided")

    data = request.data

    if (data.get("id", None) is None):
        return error_response("Invalid data")

    order: OrderRequest = OrderRequest.objects.get(pk=data.get("id"))
    order.revised_at = datetime.now()
    order.revised_by = request.user.employee
    order.status = "NG"

    try:
        denied_status = Status.objects.get(name=OrderRequest.OrderStatus.NEGATED)
    except:
        return error_response("Invalid data - status")

    status_data = {
        "created_at": datetime.now(),
        "created_by": request.user.employee.id,
        "status": denied_status.id,
        "order": order.id
    }

    order_status_serializer = CreateOrderStatusSerializer(data=status_data)

    try:
        order_status_serializer.is_valid(raise_exception=True)

    except Exception as e:
        return error_response("Invalidad data - status name")

    order_status_obj: OrderStatus = order_status_serializer.save()
    order.save()

    return response("Succesfully updated")


class SimplifiedOrderRequestView(ModelViewSet):

    queryset = (
        OrderRequest.objects.all()
        .select_related("warehouse")
        .select_related("requested_by")
        .order_by("-requested_at")
    )

    serializer_class = SimplifiedOrderSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params

        if (params.get("id", None)):
            queryset = queryset.filter(pk=params.get("id"))

        if (params.get("warehouse_id", None)):
            queryset = queryset.filter(warehouse__pk=params.get("warehouse_id"))

        if (params.get("requested_by_name", None)):
            queryset = queryset.filter(
                Q(requested_by__name__icontains=params.get("requested_by_name")) |
                Q(requested_by__lastname__icontains=params.get("requested_by_name"))
            )

        return queryset


class OrderSaveQuantityToItem(APIView):
    def get(self, request):
        try:
            ids = request.query_params.get("id")
            quantities = request.query_params.get("quantity")
            updateted_rows = OrderRequestDetail.objects.filter(item_id=ids).update(
                quantity=quantities
            )
        except Exception as e:
            error_response("Invalid query")

        return JsonResponse({"error": False, "message": "Ok"})


class OrderStatusListViewSet(ModelViewSet):
    queryset = OrderStatus.objects.all().order_by("created_at")
    serializer_class = OrderStatusSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()
        if params.get("comment", None):
            queryset = queryset.filter(comment__icontains=params.get("comment"))
        if params.get("order_id", None):
            queryset = queryset.filter(order=params.get("order_id"))

        return queryset
