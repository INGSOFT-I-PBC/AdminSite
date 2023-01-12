from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from api.models import OrderRequest
from api.models.orders import OrderRequestDetail
from api.models.products import ProductProvider
from api.models.purchases import Purchase
from api.serializers.order import (
    OrderDetailProviderProductSerializer,
    OrderDetailSerializer,
    OrderDetailSerializerprueba,
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


class OrderRequestFullView(ModelViewSet):
    queryset = OrderRequestDetail.objects.all()
    serializer_class = OrderDetailSerializerprueba

    def get_queryset(self):
        try:
            busqueda = self.request.query_params.get("busqueda")
            filtro = self.request.query_params.get("filtro")
            ids = self.request.query_params.get("id")

            if busqueda == None:
                orders_details = (
                    self.queryset.filter(
                        order_request=ids,
                    )
                    .select_related("item")
                    .select_related("item__product")
                )

            if busqueda != "":
                if busqueda != None:
                    if filtro == "marca":
                        orders_details = (
                            self.queryset.filter(
                                order_request=ids,
                                item__product__brand_name__contains=busqueda,
                            )
                            .select_related("item")
                            .select_related("item__product")
                        )

                    if filtro == "producto":
                        orders_details = (
                            self.queryset.filter(
                                order_request=ids,
                                item__product__product_name__contains=busqueda,
                            )
                            .select_related("item")
                            .select_related("item__product")
                        )

            return orders_details

        except Exception as e:
            print(e)
            return error_response("Invalid query")


class OrderRequestProductProvider(ModelViewSet):
    queryset = ProductProvider.objects.all()
    serializer_class = OrderDetailProviderProductSerializer
    """
    def get_queryset(self):
        # print(request.GET)
        try:

            orders_details = (
                self.queryset.filter(
                    order_request=self.request.query_params.get("id")
                ).select_related("product")
                # .select_related("item__category")
                .select_related("provider")
            )

            return orders_details

        except Exception as e:
            print(e)
            return error_response("Invalid query")
    """


@api_view(["GET"])
def OrderApprovePurchase(request):
    data = request.data
    oid = request.query_params.get("order_origin_id")
    order = OrderRequest.objects.filter(pk=oid).first()

    Purchase.objects.create(
        order_origin_id=oid,
        warehouse_id=order.warehouse.id,
        provider_id=1,
        reference=1,
        aproved_at="2023-01-07 12:00:00",
    )
    return error_response("Invalid query")


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
