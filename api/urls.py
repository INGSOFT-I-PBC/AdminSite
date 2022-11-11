""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views
from api.views import *
from api.views.clientview import ClientView
from api.views.itemviews import ItemView
from api.views.orders import OrderRequestView
from api.views.provinceview import ProvinceCityView
from api.views.statusview import StatusView
from api.views.warehouse import *
from api.views.invoiceview import InvoiceView,PaginatedItemInvoiceView
from api.views.sequence import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"groups/all", views.UnpaginatedGroupViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses/all", views.FullWarehouseViewSet)
router.register(r"invoices/all", views.FullInvoiceViewSet)
router.register(r"invoice/item/all", views.PaginatedIItemViewSet)
router.register(r"clients/all", views.FullClientViewSet)
router.register(r"provinces/all", views.FullProvinceViewSet)
router.register(r"gender/all", views.FullGenderViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"items", views.PaginatedItemViewSet, "paginatedItemVS")
router.register(r"invoice/item/all", views.PaginatedIItemViewSet)
router.register(r"employees", views.EmployeeViewSet, "employeeViewSet")
router.register(r"providers", views.ProviderViewSet)
router.register(r"sequence/all", views.FullSequenceViewSet)
router.register(r"payment/all", views.FullPaymentViewSet)

urlpatterns = [
    # List return paths
    path("list/", include(router.urls)),
    # Auth paths
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", self_permissions, name="user-permissions"),
    path("auth/me", user_data, name="user-data"),
    # Path for models
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    path("items", ItemView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemView.as_view(), name="item_process"),
    path("category", CategoryView.as_view(), name="category-list"),
    path("category/<int:id>", CategoryView.as_view(), name="category_process"),
    path("inventory", InventoryView.as_view(), name="inventory-list"),
    path("inventory/<int:pk>", InventoryView.as_view(), name="inventory_process"),
    path("warehouse/puchase-order", WhOrderRequestView.as_view(), name="wh-orders"),

    # Item management
    path("item/<int:id>", views.find_item, name="item"),
    path("item/<int:id>/properties", views.get_item_properties),
    # User management
    path("user/<int:id>", views.UserView.as_view()),
    path("user/<str:username>", views.UserView.as_view()),
    path("user/<int:id>/activate", views.activate_user),
    path("user/<str:username>/activate", views.activate_user),
    path("user", views.create_user),
    # Employee management
    path("employee/<int:id>", views.EmployeeView.as_view()),
    path("employee/<str:cid>", views.EmployeeView.as_view()),
    path("employee/<str:cid>/activate", views.activate_employee),
    path("employee", views.create_employee),
    # Order management
    path("order", OrderRequestView.as_view()),
    path("clients", ClientView.as_view()),
    path("status", StatusView.as_view()),
    path("provinces", ProvinceCityView.as_view()),
    # path('users'),
    # Administration endpoints
    path("admin/permission_group/<int:id>", views.PermissionGroupView.as_view()),
    path("admin/permission/<int:id>", PermissionsView.as_view()),
    path("admin/permission/<str:codename>", PermissionsView.as_view()),
    path("admin/permission", create_permission),
    # Providers endpoints
    path("provider/<int:id>", views.ProviderView.as_view()),
    path("provider", create_provider),
    path("auth/reset-password", reset_password, name="reset-user-password"),
    #Invoice
    path("invoice/client", InvoiceView.as_view({'get': 'search_client'}), name="search-invoice-client"),
    path("invoice", InvoiceView.as_view({'post': 'save_invoice'}), name="save-invoice"),

    path("invoice/editar", views.InvoicesView.as_view()),
    path("sequence", SequenceView.as_view()),
    path("invoice/item/all", PaginatedItemInvoiceView.as_view(),name="search-invoice-items")
]
