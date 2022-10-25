from api.views.authviews import (
    LogoutViewSet,
    PermissionsView,
    PermissionsViewSet,
    UserViewSet,
    reset_password,
    user_data,
)
from api.views.categoryviews import CategoryView
from api.views.inventoryviews import InventoryView
from api.views.itemview import *
from api.views.itemviews import ItemView
from api.views.warehouse import (
    FullWarehouseViewSet,
    OrderRequestViewSet,
    WarehouseView,
    WarehouseViewSet,
    WhOrderRequestView,
)

from .employee import EmployeeView  # EmployeeViewSet,; FullEmployeeViewSet,

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
    #"FullEmployeeViewSet",
    #"EmployeeViewSet",
    "EmployeeView",
]
