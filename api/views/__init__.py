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
from api.views.productInventory import *
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
    "CategoryView",
    "ClientView",
    "create_employee",
    "create_order_request",
    "create_permission",
    "create_prod_variant",
    "create_product",
    "create_provider",
    "create_purchase_status",
    "create_user",
    "CreateProductView",
    "EmployeeView",
    "EmployeeViewSet",
    "FullClientViewSet",
    "FullGenderViewSet",
    "FullInventoryViewSet2",
    "FullPaymentViewSet",
    "FullProductView",
    "FullSequenceViewSet",
    "FullWarehouseViewSet",
    "get_full_order",
    "GroupView",
    "GroupViewSet",
    "InventoryView",
    "InventoryViewSet",
    "InvoicesView",
    "InvoiceView",
    "InvoiceViewSet",
    "ItemView",
    "ItemView",
    "LogoutViewSet",
    "OrderRequestView",
    "OrderRequestViewSet",
    "OrderStatusListViewSet",
    "PaginatedIItemViewSet",
    "PaginatedItemInvoiceView",
    "PaginatedItemViewSet",
    "PermissionsView",
    "PermissionsViewSet",
    "ProductVariantView",
    "ProductVariantViewSet",
    "ProductView",
    "ProductViewSet",
    "ProviderView",
    "ProviderViewSet",
    "ProvinceCityView",
    "ProvinceViewSet",
    "PurchaseAditionalInfoViewSet",
    "PurchaseDetailsViewSet",
    "PurchaseViewSet",
    "reset_password",
    "RoleView",
    "RoleViewSet",
    "self_permissions",
    "StatusView",
    "TransactionStatusViewSet",
    "UnpaginatedGroupViewSet",
    "user_data",
    "UserView",
    "UserViewSet",
    "VariantAttributesViewSet",
    "WarehouseView",
    "WarehouseViewSet",
    "WhOrderRequestView",
    "WhProductInventoryViewSet",
]
