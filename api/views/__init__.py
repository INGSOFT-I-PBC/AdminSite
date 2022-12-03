from api.views.authviews import *
from api.views.categoryviews import CategoryView
from api.views.clientview import *
from api.views.genderview import *
from api.views.groups import *
from api.views.inventoryviews import *
from api.views.invoiceview import *
from api.views.itemview import *
from api.views.itemviews import *
from api.views.orders import *
from api.views.payment import *
from api.views.productview import *
from api.views.providers import *
from api.views.provinceview import *
from api.views.purchase import *
from api.views.roleview import *
from api.views.sequence import *
from api.views.statusview import *
from api.views.userview import *
from api.views.warehouse import *

__all__ = [
    "UserViewSet",
    "LogoutViewSet",
    "PermissionsView",
    "reset_password",
    "WarehouseView",
    "WhOrderRequestView",
    "WarehouseViewSet",
    "OrderRequestViewSet",
    "OrderRequestView",
    "ItemView",
    "CategoryView",
    "InventoryView",
    "FullInventoryViewSet2",
    "InventoryViewSet",
    "user_data",
    "PermissionsViewSet",
    "ItemView",
    "PaginatedItemViewSet",
    "FullWarehouseViewSet",
    "EmployeeView",
    "UserView",
    "create_user",
    "create_employee",
    "EmployeeViewSet",
    "self_permissions",
    "create_permission",
    "GroupViewSet",
    "UnpaginatedGroupViewSet",
    "FullClientViewSet",
    "ClientView",
    "StatusView",
    "ProvinceViewSet",
    "ProvinceCityView",
    "FullGenderViewSet",
    "InvoiceView",
    "InvoiceViewSet",
    "PaginatedItemInvoiceView",
    "InvoicesView",
    "FullSequenceViewSet",
    "FullPaymentViewSet",
    "ProviderViewSet",
    "ProviderView",
    "confirm_purchase",
    "PurchaseViewSet",
    "create_provider",
    "GroupView",
    "PaginatedIItemViewSet",
    "RoleView",
    "RoleViewSet",
    "get_full_order",
    "create_order_request",
    "ClientView",
    "InvoiceView",
    "PaginatedItemInvoiceView",
    "create_stock_barcode",
    "create_product",
    "create_prod_variant",
    "ProductVariantView",
    "ProductVariantViewSet",
    "ProductView",
    "ProductViewSet",
]
