from api.views.authviews import *
from api.views.categoryviews import CategoryView
from api.views.clientview import *
from api.views.genderview import *
from api.views.groups import *
from api.views.inventoryviews import InventoryView
from api.views.invoiceview import *
from api.views.itemview import *
from api.views.itemviews import ItemView
<<<<<<< HEAD
from api.views.payment import *
from api.views.providers import *
from api.views.provinceview import *
from api.views.roleview import *
=======
from api.views.orders import *
from api.views.payment import *
from api.views.providers import *
from api.views.provinceview import *
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27
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
    "ItemView",
    "CategoryView",
    "InventoryView",
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
    "StatusView",
    "ProvinceViewSet",
    "ProvinceCityView",
    "FullGenderViewSet",
    "FullInvoiceViewSet",
    "InvoicesView",
    "FullSequenceViewSet",
    "FullPaymentViewSet",
    "ProviderViewSet",
    "ProviderView",
    "create_provider",
    "GroupView",
    "PaginatedIItemViewSet",
<<<<<<< HEAD
    "RoleView",
    "RoleViewSet",
=======
    "get_full_order",
    "create_order_request",
>>>>>>> 834b2935bcb85526036eb66b0e2eb6e153be5f27
]
