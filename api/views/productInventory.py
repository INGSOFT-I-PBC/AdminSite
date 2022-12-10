from datetime import datetime, timedelta

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models.products import ProductStockWarehouse
from api.serializers.warehouse import WhStockSerializer


class CustomPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "page": self.page.number,
                "lastPage": self.page.paginator.num_pages,
                "total": self.page.paginator.count,
            }
        )


class WhProductInventoryViewSet(ModelViewSet):
    pagination_class = CustomPagination
    queryset = ProductStockWarehouse.objects.all().order_by("-id")
    serializer_class = WhStockSerializer

    def get_queryset(self):

        queryset = self.queryset.exclude(product__active=0)
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("id", None):
            queryset = queryset.filter(id=params.get("id", None))
            return queryset

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse_id=params.get("warehouse_id")
            ).prefetch_related("product")

        if params.get("name", None):
            queryset = queryset.filter(
                Q(product__variant_name__icontains=params.get("name"))
                | Q(product__product__product_name__icontains=params.get("name"))
            )

        if params.get("short_description", None):
            queryset = queryset.filter(
                product__product__summary__icontains=params.get("short_description")
            )

        if params.get("sku", None):
            queryset = queryset.filter(product__sku__icontains=params.get("sku"))

        if params.get("min_quantity", None):
            queryset = queryset.filter(quantity__gte=params.get("min_quantity"))

        if params.get("max_quantity", None):
            queryset = queryset.filter(quantity__lte=params.get("max_quantity"))

        if params.get("min_price", None):
            queryset = queryset.filter(product__price__gte=params.get("min_price"))

        if params.get("max_price", None):
            queryset = queryset.filter(product__price__lte=params.get("max_price"))

        if params.get("min_base", None):
            queryset = queryset.filter(
                product____product__base_price__gte=params.get("min_price")
            )

        if params.get("max_base", None):
            queryset = queryset.filter(
                product____product__base_price__lte=params.get("min_price")
            )

        if params.get("from_date", None):
            queryset = queryset.filter(updated_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)

            queryset = queryset.filter(updated_at__lte=to_date)

        return queryset
