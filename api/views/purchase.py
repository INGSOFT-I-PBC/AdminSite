from datetime import datetime, timedelta

from django.db.models import OuterRef, Subquery
from django.db.models.aggregates import Max
from django.db.models.expressions import F
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Purchase, User
from api.models.common import Status
from api.models.purchases import PurchaseChild, PurchaseDetail, PurchaseStatus
from api.serializers.purchase import (
    PurchaseAditionalInfoSerialzier,
    PurchaseDetailSerializer,
    PurchaseStatusSerializer,
    SavePurchaseStatusSerializer,
)
from api.utils import error_response


class CustomPagination(PageNumberPagination):
    page_size = 1000
    page_size_query_param = "per_page"

    def get_paginated_response(self, data):
        return Response(
            {
                "data": data,
                "lastPage": self.page.paginator.num_pages,
                "page": self.page.number,
                "total": self.page.paginator.count,
            }
        )


class PurchaseViewSet(ModelViewSet):
    """
    API endpoint that allows purchases to be viewed.
    """

    queryset = Purchase.objects.all().order_by("-approved_at")
    serializer_class = PurchaseStatusSerializer

    def get_queryset(self):
        queryset = self.queryset.select_related("order_origin")
        params = self.request.query_params.copy()

        queryset = queryset.annotate(
            status=Subquery(
                PurchaseStatus.objects.filter(purchase=OuterRef("id"))
                .order_by("-created_at")
                .select_related("status")
                .values("status__name")[:1]
            )
        )

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("purchase_id", None):
            queryset = queryset.filter(id=params.get("purchase_id"))
            return queryset

        if params.get("reference", None):
            queryset = queryset.filter(reference=params.get("reference"))
            return queryset

        if params.get("invoice_id", None):
            queryset = queryset.filter(
                id__in=Subquery(
                    PurchaseChild.objects.filter(
                        invoice__id=(params.get("invoice_id").values("purchase_header"))
                    )
                )
            )
            return queryset

        if params.get("order_id", None):
            queryset = queryset.filter(order_origin__id=params.get("order_id"))
            return queryset

        if params.get("invoice_code", None):
            queryset = queryset.filter(
                invoice__code__icontains=params.get("invoice_code")
            )

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).prefetch_related("warehouse")

        if params.get("warehouse_name", None):
            queryset = queryset.filter(
                warehouse__name__icontains=params.get("warehouse_name")
            )

        if params.get("status", None):

            p_status = (
                PurchaseStatus.objects.annotate(
                    last_status_pk=Max("purchase__purchasestatus__pk")
                )
                .filter(pk=F("last_status_pk"))
                .filter(status__name__icontains=params.get("status"))
            )

            if params.get("status_from_date", None):
                p_status = p_status.filter(
                    created_at__gte=params.get("status_from_date")
                )

            if params.get("status_to_date", None):
                to_date = datetime.strptime(
                    (params.get("status_to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
                ) + timedelta(days=1)

                p_status = p_status.filter(created_at__gte=to_date)

            queryset = queryset.filter(pk__in=Subquery(p_status.values("purchase")))

        if params.get("provider_name", None):
            queryset = queryset.filter(
                id__in=Subquery(
                    PurchaseChild.objects.filter(
                        provider__name__icontains=params.get("provider_header").values(
                            "purchase"
                        )
                    )
                )
            )

        if params.get("from_date", None):
            if params.get("invoice_date", None):
                queryset = queryset.filter(
                    id__in=Subquery(
                        PurchaseChild.objects.filter(
                            invoice__created_at__gte=(
                                params.get("from_date").values("purchase_header")
                            )
                        )
                    )
                )
            if params.get("approved_date", None):
                queryset = queryset.filter(approved_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)

            if params.get("invoice_date", None):
                queryset = queryset.filter(
                    id__in=Subquery(
                        PurchaseChild.objects.filter(
                            invoice__created_at__lte=(
                                params.get("from_date").values("purchase_header")
                            )
                        )
                    )
                )
            if params.get("approved_date", None):
                queryset = queryset.filter(approved_at__lte=to_date)

        return queryset


class PurchaseAditionalInfoViewSet(PurchaseViewSet):
    """Inherits PurchaseViewSet
    Provides more details of the purchase after filtering
    """

    serializer_class = PurchaseAditionalInfoSerialzier

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset.select_related("warehouse")

        return queryset


class PurchaseDetailsViewSet(ModelViewSet):

    queryset = PurchaseDetail.objects.all().order_by("-id")
    serializer_class = PurchaseDetailSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if (
            params.get("purchase_id", None)
            and params.get("invoice_id", None)
            and params.get("purchase_child_id", None)
        ):
            return error_response("Invalid request")

        if params.get("purchase_id", None):
            purchase = Purchase.objects.get(
                id=params.get("purchase_id")
            ).prefetch_realted("purchase_child")
            queryset = queryset.filter(
                purchase_child__in=Subquery(
                    PurchaseChild.objects.filter(purchase=purchase)
                )
            )
        if params.get("purchase_child_id", None):
            queryset = queryset.filter(purchase_child=params.get("purchase_child_id"))
            return queryset

        return queryset


@api_view(["POST"])
def create_purchase_status(request):
    """Creates a status for the Purchase Model

    Args:
        request: Post request

    Returns:
       Success: The purchase_status object data, http status code 201
       Failure: The Json error response with error code 400
    """
    if not request.data:
        return error_response("No data was provided")

    if not request.data.get("id") or not request.data.get("status"):
        return error_response("Incomplete data")

    id = int(request.data.get("id"))
    purchase = Purchase.objects.get(pk=id)
    status_obj = Status.objects.filter(name=request.data.get("status")).first()
    employee = User.objects.get(id=request.user.id).employee

    data = {
        "created_at": datetime.now(),
        "created_by": employee.id,
        "purchase": purchase.id,
        "status": status_obj.id,
    }

    serializer = SavePurchaseStatusSerializer(data=data)
    if serializer.is_valid(raise_exception=True):
        if request.data.get("status") == "entregado":
            purchase_childs = PurchaseChild.objects.filter(
                purchase_header=request.data.get("id")
            )
            purchase_childs.update(is_delivered=True)

        if request.data.get("status") == "pagado":
            purchase_childs = PurchaseChild.objects.filter(
                purchase_header=request.data.get("id")
            )
            purchase_childs.update(is_purchased=True)

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return error_response("Invalid data")
