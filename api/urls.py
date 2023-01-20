""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views
from api.views.warehouse import TransactionStatusViewSet, WhTransactionDetailsViewSet

""" Definition of paginated data
 This urls are read-only, for batch creation/update
 an specialized route must be created on the  `urlpatterns` field
"""
router = routers.DefaultRouter(trailing_slash=False)
router.register("product/(?P<product>\d+)/variants", views.ProductVariantViewSet)
router.register("purchase", views.PurchaseViewSet),
router.register(r"clients/all", views.ClientViewSet)
router.register(r"employees", views.EmployeeViewSet, "employeeViewSet")
router.register(r"gender/all", views.FullGenderViewSet)
router.register(r"groups/all", views.UnpaginatedGroupViewSet)
router.register(r"groups", views.GroupViewSet)
router.register(r"inventory/all", views.FullInventoryViewSet, "paginatedInventoryVS")
router.register(r"inventory", views.InventoryViewSet)
router.register(r"invoice/item/all", views.PaginatedIItemViewSet)
router.register(r"items", views.PaginatedItemViewSet, "paginatedItemVS")
router.register(r"payment/all", views.FullPaymentViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"products/variants", views.ProductVariantViewSet)
router.register(r"products", views.ProductViewSet)
router.register(r"provinces/all", views.FullProvinceViewSet)
router.register(r"providers", views.ProviderViewSet)
router.register(r"roles", views.RoleViewSet, "roleViewSet")
router.register(r"sequence/all", views.FullSequenceViewSet)
router.register(r"users", views.UserViewSet)
router.register(r"warehouses/all", views.FullWarehouseViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses/order-requests2", views.SimplifiedOrderRequestView)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"products/variants/<int:variant>/stock", views.ProductStockViewSet)
router.register(r"products/barcode-data/variants", views.ProductVariantsViewSet)
router.register("products/(?P<product>\d+)/stock", views.ProductVariantViewSet)


urlpatterns = [
    # List return paths
    path("list/", include(router.urls)),
    # =====================================
    # <|            Auth endpoints       |>
    # =====================================
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", views.self_permissions, name="user-permissions"),
    path("auth/me", views.user_data, name="user-data"),
    # =====================================
    # <|        Administrarion endpoints |>
    # =====================================
    path("admin/permission", views.create_permission),
    path("admin/permission/<int:id>", views.PermissionsView.as_view()),
    path("admin/permission/<str:codename>", views.PermissionsView.as_view()),
    path("admin/permission_group/<int:id>", views.PermissionGroupView.as_view()),
    # =====================================
    # <|        Employee endpoints       |>
    # =====================================
    path("employee", views.create_employee),
    path("employee/<int:id>", views.EmployeeView.as_view()),
    path("employee/<str:cid>", views.EmployeeView.as_view()),
    path("employee/<str:cid>/activate", views.activate_employee),
    path("employee/<str:cid>/inactivate", views.inactivate_employee),
    # =====================================
    # <|       Category  endpoints       |>
    # =====================================
    path("category", views.CategoryView.as_view(), name="category-list"),
    path("category/<int:id>", views.CategoryView.as_view(), name="category_process"),
    # =====================================
    # <|        Clients  endpoints       |>
    # =====================================
    path("clients", views.ClientView.as_view()),
    # =====================================
    # <|        Invoice  endpoints       |>
    # =====================================
    path(
        "invoices",
        views.InvoiceViewSet.as_view({"get": "list"}),
        name="invoices",
    ),
    path(
        "invoice/client",
        views.InvoiceView.as_view({"get": "search_client"}),
        name="search-invoice-client",
    ),
    path("invoice", views.InvoiceView.as_view({"post": "save_invoice"}), name="save-invoice"),
    path(
        "invoice/quantity",
        views.InvoiceView.as_view({"put": "edit_quantity"}),
        name="save-invoice",
    ),
    path(
        "invoice/details/item",
        views.InvoiceView.as_view({"get": "search_item"}),
        name="search-details-invoice",
    ),
    path("invoice/editar", views.InvoicesView.as_view()),
    path("sequence", views.SequenceView.as_view()),
    path(
        "invoice/item/all",
        views.PaginatedItemInvoiceView.as_view(),
        name="search-invoice-items",
    ),
    # =====================================
    # <|        Inventory endpoints       |>
    # =====================================
    path("inventory", views.InventoryView.as_view(), name="inventory-list"),
    path("inventory/<int:pk>", views.InventoryView.as_view(), name="inventory_process"),
    path(
        "inventories",
        views.FullInventoryViewSet2.as_view({"get": "list"}),
    ),
    # =====================================
    # <|        Times endpoints           |>
    # =====================================
    path("items", views.ItemView.as_view(), name="item-list"),
    path("items/<int:id>", views.ItemView.as_view()),
    path("item/<int:id>/activate", views.activate_item),
    path("item/<int:id>/inactivate", views.inactivate_item),
    path("item/<int:id>", views.find_item, name="item"),
    path("item/<int:id>/properties", views.get_item_properties),
    # =====================================
    # <|        order endpoints       |>
    # =====================================
    path("detailed/order/<int:id>", views.get_full_order),
    path("order", views.create_order_request),
    path("order/<int:id>", views.OrderRequestView.as_view()),
    path("order/status", views.OrderStatusListViewSet.as_view({"get": "list"})),
    path("order/reject", views.reject_order),
    path(
        "order/details",
        views.OrderRequestDetailFullView.as_view({"get": "list"}),
        name="order-details",
    ),
    path("provinces", views.ProvinceCityView.as_view()),
    path("status", views.StatusView.as_view()),
    # =====================================
    # <|        Provider endpoints       |>
    # =====================================
    path("provider/<int:id>", views.ProviderView.as_view()),
    path("provider", views.create_provider),
    path("auth/reset-password", views.reset_password, name="reset-user-password"),
    # =====================================
    # <|        Product endpoints        |>
    # =====================================
    path("product", views.CreateProductView.as_view()),
    path("products/variant", views.create_prod_variant),
    path("products/variant/props", views.VariantAttributesViewSet.as_view({"get": "list"})),
    path("product/<int:pk>", views.FullProductView.as_view()),
    path("product/<int:product>/variant/<str:sku>", views.ProductVariantView.as_view()),
    path("product/<int:product>/variant/<int:id>", views.ProductVariantView.as_view()),
    path("products/variant/<str:sku>", views.ProductVariantView.as_view()),
    # =====================================
    # <|        Purchase endpoints       |>
    # =====================================
    path("purchase/create", views.create_purchase),
    path("purchase/details", views.PurchaseDetailsViewSet.as_view({"get": "list"})),
    path("purchase", views.PurchaseAditionalInfoViewSet.as_view({"get": "list"})),
    # =====================================
    # <|         Movement endpoints       |>
    # =====================================
    path("movement/status", TransactionStatusViewSet.as_view({"get": "list"})),
    path("movement", WhTransactionDetailsViewSet.as_view({"get": "list"})),
    path('movement/create', views.create_movement),
    path('movement/compromised-stock', views.WhStockWithCompromiesd.as_view({"get": "list"})),
    # =====================================
    # <|        Role endpoints       |>
    # =====================================
    path("role", views.create_role),
    path("role/<int:id>", views.RoleView.as_view()),
    path("role/<str:id>", views.RoleView.as_view()),
    # =====================================
    # <|        Warehouse endpoints       |>
    # =====================================
    path("warehouse", views.WarehouseView.as_view(), name="warehouse-list"),
    path("warehouse/order", views.WhOrderRequestView.as_view(), name="wh-orders"),
    path(
        "warehouse/stock",
        views.WhStockViewSet.as_view({"get": "list"}),
        name="wh-inventory",
    ),
    path(
        "warehouse/stock-props",
        views.WhStockWithPropsViewSet.as_view({"get": "list"}),
        name="wh-stock-props",
    ),
    path("warehouse/purchase/confirm", views.create_purchase_status),
    path(
        "warehouse/purchase",
        views.PurchaseViewSet.as_view({"get": "list"}),
        name="wh-purchase",
    ),
    path(
        "warehouse/purchase/status",
        views.create_purchase_status,
        name="wh-confirm-purchase",
    ),
    path(
        "warehouse/movements",
        views.WhTransactionViewSet.as_view({"get": "list"}),
        name="wh-movements",
    ),
    path("warehouse/puchase-order", views.WhOrderRequestView.as_view(), name="wh-orders"),
    path(
        "warehouse/tomas-fisicas",
        views.WhTomasFisicasViewSet.as_view({"get": "list", "post": "create_toma_fisica"}),
        name="wh-tomas",
    ),
    # Tomas fisicas
    path(
        "warehouse/tomas-fisicas/update-stock", views.update_stock,
        name="wh-tomas-update-stock",
    ),
    path(
        "warehouse/tomas-fisicas/details",
        views.TomasFisicasDetailsViewSet.as_view({"get": "list"}),
        name="wh-tomas-details",
    ),


    path(
        "warehouse/tomas-fisicas/all",
        views.WhLatestTomaFisicaView.as_view(),
        name="all-wh-tomas",
    ),
    # Product Variant inventory
    path(
        "warehouse/product-inventory",
        views.WhProductInventoryViewSet.as_view({"get": "list"}),
        name="product-inventory",
    ),
    path("warehouse/puchase-order", views.WhOrderRequestView.as_view(), name="wh-orders"),
    # =====================================
    # <|         User endpoints          |>
    # =====================================
    path("user/<int:id>", views.UserView.as_view()),
    path("user/<str:username>", views.UserView.as_view()),
    path("user/<int:id>/activate", views.activate_user),
    path("user/<str:username>/activate", views.activate_user),
    path("user", views.create_user),

    # -====[ Test Api view urls ]====-
    path("utils/test", views.CreateTestView.as_view()),
    re_path(r"utils/test/(?P<id>\d+)", views.TestAPIView.as_view()),
]
