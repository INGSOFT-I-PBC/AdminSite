from datetime import datetime, timedelta

from django.db.models import OuterRef, Subquery
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Purchase
from api.models.common import Status
from api.models.purchases import PurchaseStatus
from api.serializers.purchase import PurchaseStatusSerializer, StatusPurchaseSerializer
from api.utils import error_response


class PurchaseViewSet(ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """

    queryset = Purchase.objects.all().order_by("-aproved_at")
    serializer_class = PurchaseStatusSerializer

    def get_queryset(self):
        queryset = self.queryset
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("reference", None):
            queryset = queryset.filter(reference=params.get("reference"))

        if params.get("invoice_id", None):
            queryset = queryset.filter(invoice=params.get("invoice_id"))
            return queryset

        if params.get("invoice_code", None):
            queryset = queryset.filter(
                invoice__code__icontains=params.get("invoice_code")
            )

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).prefetch_related("warehouse", "provider", "invoice")

        if params.get("warehouse_name", None):
            queryset = queryset.filter(
                warehouse__name__icontains=params.get("warehouse_name")
            )

        if params.get("status", None):
            purchase_status = PurchaseStatus.objects.filter(
                status__name__icontains=params.get("status")
            ).order_by("-created_at")

            queryset = queryset.filter(
                id=Subquery(purchase_status.values("purchase")[:1])
            )

        if params.get("provider_name", None):
            queryset = queryset.filter(
                provider__name__icontains=params.get("provider_name")
            )

        if params.get("from_date", None):
            if params.get("invoice_date", None):
                queryset = queryset.filter(
                    invoice__created_at__gte=(params["from_date"])
                )
            if params.get("aproved_date", None):
                queryset = queryset.filter(aproved_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = datetime.strptime(
                (params.get("to_date")), "%Y-%m-%dT%H:%M:%S.%f%z"
            ) + timedelta(days=1)

            if params.get("invoice_date", None):
                queryset = queryset.filter(invoice__created_at__lte=to_date)
            if params.get("aproved_date", None):
                queryset = queryset.filter(aproved_at__lte=to_date)

        queryset = queryset.annotate(
            status=Subquery(
                PurchaseStatus.objects.filter(purchase=OuterRef("id"))
                .order_by("-created_at")
                .values("status__name")[:1]
            )
        )

        return queryset


@api_view(["POST"])
def confirm_purchase(request):
    if not request.data:
        return error_response("No data was provided")

    if not request.data.get("id") or not request.data.get("status"):
        return error_response("Incomplete data")

    id = int(request.data.get("id"))
    purchase = Purchase.objects.filter(pk=id).first()
    status_obj = Status.objects.filter(name=request.data.get("status")).first()

    data = {
        "purchase": purchase.id,
        "status": status_obj.id,
        "created_by": request.user.id,
        "created_at": datetime.now(),
    }

    serializer = StatusPurchaseSerializer(data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
