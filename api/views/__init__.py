from api.views.authviews import *
from api.views.categoryviews import CategoryView
from api.views.clientview import *
from api.views.groups import *
from api.views.inventoryviews import InventoryView
from api.views.itemview import *
from api.views.itemviews import ItemView
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
]
