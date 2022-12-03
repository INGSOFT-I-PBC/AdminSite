""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views
from api.views import *
from api.views.sequence import *
from api.views.warehouse import *

""" Definition of paginated data
 This urls are read-only, for batch creation/update
 an specialized route must be created on the  `urlpatterns` field
"""
router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"groups/all", views.UnpaginatedGroupViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses/all", views.FullWarehouseViewSet)
router.register(r"invoice/item/all", views.PaginatedIItemViewSet)
router.register(r"clients/all", views.ClientViewSet)
router.register(r"provinces/all", views.FullProvinceViewSet)
router.register(r"gender/all", views.FullGenderViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"items", views.PaginatedItemViewSet, "paginatedItemVS")
router.register(r"inventory/all", views.FullInventoryViewSet, "paginatedInventoryVS")
router.register(r"employees", views.EmployeeViewSet, "employeeViewSet")
router.register(r"roles", views.RoleViewSet, "roleViewSet")
router.register(r"providers", views.ProviderViewSet)
router.register("purchase", views.PurchaseViewSet),
router.register(r"sequence/all", views.FullSequenceViewSet)
router.register(r"payment/all", views.FullPaymentViewSet)
router.register(r"inventory", views.InventoryViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"product/<int:pk>/variants", views.ProductVariantViewSet)
router.register(r"products/variants", views.ProductVariantViewSet)


urlpatterns = [
    # List return paths
    path("list/", include(router.urls)),
    # Auth paths
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", self_permissions, name="user-permissions"),
    path("auth/me", user_data, name="user-data"),
    # Path for models
    #
    #### Warehouse related
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    # path("warehouse/<int:warehouse>/barcodes"),
    path("warehouse/<int:warehouse>/barcode/<int:pk>", views.BarcodeView.as_view()),
    path("warehouse/<int:warehouse>/barcode/<str:label>", views.BarcodeView.as_view()),
    path("warehouse/barcode", create_stock_barcode),
    #
    #### Items related
    path("warehouse/order", WhOrderRequestView.as_view(), name="wh-orders"),
    path(
        "warehouse/inventory",
        WhInventorysViewSet.as_view({"get": "list"}),
        name="wh-inventory",
    ),
    path(
        "warehouse/purchase",
        PurchaseViewSet.as_view({"get": "list"}),
        name="wh-purchase",
    ),
    path(
        "warehouse/purchase/confirm",
        confirm_purchase,
        name="wh-confirm-purchase",
    ),
    path(
        "warehouse/movements",
        WhTransactionViewSet.as_view({"get": "list"}),
        name="wh-movements",
    ),
    path("warehouse/puchase-order", WhOrderRequestView.as_view(), name="wh-orders"),
    path(
        "warehouse/tomas-fisicas",
        WhTomasFisicasViewSet.as_view({"get": "list"}),
        name="wh-tomas",
    ),
    path(
        "warehouse/tomas-fisicas/all",
        WhLatestTomaFisicaView.as_view(),
        name="all-wh-tomas",
    ),
    path("items", ItemView.as_view(), name="item-list"),
    path("items/<int:id>", views.ItemView.as_view()),
    path("item/<int:id>/activate", views.activate_item),
    path("item/<int:id>/inactivate", views.inactivate_item),
    path("category", CategoryView.as_view(), name="category-list"),
    path("category/<int:id>", CategoryView.as_view(), name="category_process"),
    path("item/<int:id>", views.find_item, name="item"),
    path("item/<int:id>/properties", views.get_item_properties),
    #
    #### Inventory related
    path("inventory", InventoryView.as_view(), name="inventory-list"),
    path("inventory/<int:pk>", InventoryView.as_view(), name="inventory_process"),
    path(
        "inventories",
        FullInventoryViewSet2.as_view({"get": "list"}),
    ),
    path("warehouse/puchase-order", WhOrderRequestView.as_view(), name="wh-orders"),
    #
    # User management
    path("user/<int:id>", views.UserView.as_view()),
    path("user/<str:username>", views.UserView.as_view()),
    path("user/<int:id>/activate", views.activate_user),
    path("user/<str:username>/activate", views.activate_user),
    path("user", views.create_user),
    #
    # Employee management
    path("employee", views.create_employee),
    path("employee/<int:id>", views.EmployeeView.as_view()),
    path("employee/<str:cid>", views.EmployeeView.as_view()),
    path("employee/<str:cid>/activate", views.activate_employee),
    path("employee/<str:cid>/inactivate", views.inactivate_employee),
    #
    # Order management
    path("order/<int:id>", WhOrderRequestView.as_view()),
    path("order", create_order_request),
    path("detailed/order/<int:id>", views.get_full_order),
    path("clients", ClientView.as_view()),
    path("status", StatusView.as_view()),
    path("provinces", ProvinceCityView.as_view()),
    #
    # Administration endpoints
    path("admin/permission_group/<int:id>", views.PermissionGroupView.as_view()),
    path("admin/permission/<int:id>", PermissionsView.as_view()),
    path("admin/permission/<str:codename>", PermissionsView.as_view()),
    path("admin/permission", create_permission),
    path("role/<int:id>", views.RoleView.as_view()),
    #
    # Providers endpoints
    path("provider/<int:id>", views.ProviderView.as_view()),
    path("provider", create_provider),
    path("auth/reset-password", reset_password, name="reset-user-password"),
    #
    # Role management
    path("role", views.create_role),
    path("role/<int:id>", views.RoleView.as_view()),
    path("role/<str:id>", views.RoleView.as_view()),
    # Invoice
    path(
        "invoices",
        InvoiceViewSet.as_view({"get": "list"}),
        name="invoices",
    ),
    path(
        "invoice/client",
        InvoiceView.as_view({"get": "search_client"}),
        name="search-invoice-client",
    ),
    path("invoice", InvoiceView.as_view({"post": "save_invoice"}), name="save-invoice"),
    path(
        "invoice/quantity",
        InvoiceView.as_view({"put": "edit_quantity"}),
        name="save-invoice",
    ),
    path(
        "invoice/details/item",
        InvoiceView.as_view({"get": "search_item"}),
        name="search-details-invoice",
    ),
    path("invoice/editar", views.InvoicesView.as_view()),
    path("sequence", SequenceView.as_view()),
    path(
        "invoice/item/all",
        PaginatedItemInvoiceView.as_view(),
        name="search-invoice-items",
    ),
    # =============================
    # >     Product endpoints     <
    # =============================
    path("product", create_product),
    path("product/variant", create_prod_variant),
    path("product/<int:pk>", ProductView.as_view()),
    path("product/variant/<int:pk>", ProductVariantView.as_view()),
    path("product/variant/<str:sku>", ProductVariantView.as_view()),
]
