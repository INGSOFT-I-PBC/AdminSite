from datetime import datetime

from rest_framework.viewsets import ModelViewSet

from api.models import Purchase
from api.serializers.purchase import PurchaseSerializer


class PurchaseViewSet(ModelViewSet):
    """
    API endpoint that allows purchases to be viewed or edited.
    """

    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def get_queryset(self):
        queryset = Purchase.objects.all()
        params = self.request.query_params.copy()

        if params.get("order_by", None):
            fields = params.pop("order_by")
            queryset = queryset.order_by(*fields)

        if params.get("invoice_id", None):
            queryset = queryset.filter(invoice=params.get("invoice_id"))
            return queryset

        if params.get("invoice_code", None):
            queryset = queryset.filter(invoice__code=params.get("invoice_code"))
            return queryset

        if params.get("warehouse_id", None):
            queryset = queryset.filter(
                warehouse=params.get("warehouse_id")
            ).prefetch_related("warehouse", "provider", "invoice")

        if params.get("warehouse_name", None):
            queryset = queryset.filter(
                warehouse__name__icontains=params.get("warehouse_name")
            )

        if params.get("status", None):
            queryset = queryset.filter(status__name__icontains=params.get("status"))

        if params.get("from_date", None):
            if params.get("invoice_date", None):
                queryset = queryset.filter(
                    invoice__created_at__gte=(params["from_date"])
                )
            if params.get("aproved_date", None):
                queryset = queryset.filter(aproved_at__gte=(params["from_date"]))

        if params.get("to_date", None):
            to_date = params.get("to_date", None) + datetime.timedelta(days=1)

            if params.get("invoice_date", None):
                queryset = queryset.filter(invoice__created_at__lte=to_date)
            if params.get("aproved_date", None):
                queryset = queryset.filter(aproved_at__lte=to_date)

        return queryset
