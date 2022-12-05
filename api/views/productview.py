from datetime import datetime

from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.filters import OrderingFilter
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.request import Request
from rest_framework.views import APIView as _APIView
from rest_framework.viewsets import ReadOnlyModelViewSet as _ROViewSet

from api.models.products import Product, ProductVariant
from api.serializers.product import (
    InputProductSerializer,
    ProductSerializer,
    ProductVariantSerializer,
)
from api.utils import error_response, response


class ProductViewSet(_ROViewSet):
    queryset = Product.objects.filter(is_active=True).order_by("product_name")
    serializer_class = ProductSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["product_name", "summary", "brand_name", "base_price"]


class ProductVariantViewSet(_ROViewSet):
    queryset = ProductVariant.objects.order_by("variant_name")
    serializer_class = ProductVariantSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ["variant_name", "sku", "price"]

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()
        if not params.get("all", False):
            queryset.filter(active=True)
        product_id = self.kwargs.get("product", None)
        if product_id is not None:
            queryset.filter(product=product_id)
        return queryset


class CreateProductView(CreateAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = InputProductSerializer


class FullProductView(RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.filter(is_active=True)
    serializer_class = ProductSerializer


class ProductView(_APIView):
    def get(self, request: Request, *args, **kwargs):
        query = Product.objects.filter(**kwargs, is_active=True)
        if not query.exists():
            return error_response("Product not found", "PROD_NOT_FOUND", status=404)
        return JsonResponse(data=ProductSerializer(query.first()).data)

    def put(self, request: Request, *args, **kwargs):
        query = Product.objects.filter(**kwargs, is_active=True)
        if not query.exists():
            return error_response("Product not found", "PROD_NOT_FOUND", status=404)
        data = request.data
        if not data:
            return error_response("No data to update", "NO_DATA")
        target = query.first()
        serial = ProductSerializer(data=data)
        serial.is_valid(raise_exception=True)
        target = serial.update(target)
        target.updated_at = datetime.now()
        target.save()
        return response("Product updated corrected", "SUCC_UPDATE")

    def delete(self, request: Request, *args, **kwargs):
        query = Product.objects.filter(**kwargs, is_active=True)
        if not query.exists():
            return error_response("Product not found", "PROD_NOT_FOUND", status=404)
        target = query.first()
        target.deleted_at = datetime.now()
        target.is_active = False
        target.save()
        return response("Product deleted correctly")


class ProductVariantView(_APIView):
    def get(self, request: Request, *args, **kwargs):
        query = ProductVariant.objects.filter(**kwargs)
        if not query.exists():
            return error_response(
                "Product variant not found", "PRODV_NOT_FOUND", status=404
            )
        return JsonResponse(data=ProductVariantSerializer(query.first()).data)

    def put(self, request: Request, *args, **kwargs):
        pass

    def delete(self, request: Request, *args, **kwargs):
        pass


@api_view(["POST"])
def create_product(request: Request):
    pass


@api_view(["POST"])
def create_prod_variant(request: Request):
    pass
