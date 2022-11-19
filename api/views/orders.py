from django.http import JsonResponse
from rest_framework.request import Request
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from api.models import OrderRequest
from api.models.orders import OrderRequestDetail
from api.serializers.order import OrderDetailSerializer, OrderSerializer
from api.utils import error_response


class OrderRequestView(APIView):
    def get(self, request: Request):
        try:
            id = int(request.GET.get("id"))
            order = OrderRequest.objects.filter(pk=id).first()
            if order is None:
                return error_response("Not found", status=404)
            serializer = OrderSerializer(order)
            return JsonResponse(serializer.data)
        except TypeError:
            return error_response("invalid params")

    def post(self, request: Request):
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
            return JsonResponse(serializer.data)
        return error_response("The given data was invalid")


class OrderRequestFullView(ModelViewSet):
    queryset = OrderRequestDetail.objects.all()
    serializer_class = OrderDetailSerializer

    def get_queryset(self):
        # print(request.GET)
        try:

            orders_details = self.queryset.filter(
                order_request=self.request.query_params.get("id")
            ).select_related("item")

            return orders_details

        except Exception as e:
            print(e)
            return error_response("Invalid query")
