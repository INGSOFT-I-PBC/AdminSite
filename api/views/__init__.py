# from api.views.authviews import *
from api.views.authviews import (
    EmployeeViewSet,
    LogoutViewSet,
    PermissionGroupView,
    PermissionsView,
    PermissionsViewSet,
    UserViewSet,
    create_permission,
    reset_password,
    self_permissions,
    user_data,
)
from api.views.categoryviews import CategoryView
from api.views.clientview import ClientView, ClientViewSet, FullClientViewSet
from api.views.genderview import FullGenderViewSet, GenderView
from api.views.groups import GroupView, GroupViewSet, UnpaginatedGroupViewSet
from api.views.inventoryviews import (
    FullInventoryViewSet,
    FullInventoryViewSet2,
    InventoryView,
    InventoryViewSet,
)
from api.views.invoiceview import (
    InvoicesView,
    InvoiceView,
    InvoiceViewSet,
    PaginatedIItemViewSet,
    PaginatedItemInvoiceView,
)
from api.views.itemview import (
    ItemView,
    ItemViewSet,
    PaginatedItemViewSet,
    find_item,
    get_item_properties,
)
from api.views.itemviews import activate_item, inactivate_item
from api.views.orders import (
    OrderApprovePurchase,
    OrderRequestFullView,
    OrderRequestView,
    OrderRequestViewSet,
    OrderStatusListViewSet,
    create_order_request,
    get_full_order,
)
from api.views.payment import FullPaymentViewSet, PaymentView, PaymentViewSet
from api.views.productInventory import WhProductInventoryViewSet
from api.views.productview import (
    CreateProductView,
    FullProductView,
    ProductStockViewSet,
    ProductVariantView,
    ProductVariantViewSet,
    ProductView,
    ProductViewSet,
    VariantAttributesViewSet,
    create_prod_variant,
    create_product,
)
from api.views.providers import ProviderView, ProviderViewSet, create_provider
from api.views.provinceview import (
    FullProvinceViewSet,
    ProvinceCityView,
    ProvinceViewSet,
)
from api.views.purchase import (
    PurchaseAditionalInfoViewSet,
    PurchaseDetailsViewSet,
    PurchaseViewSet,
    create_purchase,
    create_purchase_status,
)
from api.views.roleview import RoleView, RoleViewSet, create_role
from api.views.sequence import FullSequenceViewSet, SequenceView, SequenceViewSet
from api.views.statusview import StatusView
from api.views.test import CreateTestView, TestAPIView
from api.views.userview import (
    EmployeeView,
    UserView,
    activate_employee,
    activate_user,
    create_employee,
    create_user,
    inactivate_employee,
)
from api.views.warehouse import (
    FullWarehouseViewSet,
    OrderRequestViewSet2,
    OrderSavePriceToItem,
    TomasFisicasDetailsViewSet,
    TransactionStatusViewSet,
    WarehouseView,
    WarehouseViewSet,
    WhLatestTomaFisicaView,
    WhOrderRequestView,
    WhOrderRequestViewSet,
    WhStockViewSet,
    WhStockWithPropsViewSet,
    WhTomasFisicasViewSet,
    WhTransactionDetailsViewSet,
    WhTransactionViewSet,
    create_movement,
)

__all__ = [
    activate_employee,
    activate_item,
    activate_user,
    CategoryView,
    ClientView,
    ClientViewSet,
    create_employee,
    create_order_request,
    create_permission,
    create_movement,
    create_prod_variant,
    create_product,
    create_provider,
    create_purchase,
    create_purchase_status,
    create_role,
    create_user,
    CreateProductView,
    EmployeeView,
    EmployeeViewSet,
    find_item,
    FullClientViewSet,
    FullGenderViewSet,
    FullInventoryViewSet,
    FullInventoryViewSet2,
    FullPaymentViewSet,
    FullProductView,
    FullProvinceViewSet,
    FullSequenceViewSet,
    FullWarehouseViewSet,
    GenderView,
    get_full_order,
    get_item_properties,
    GroupView,
    GroupViewSet,
    inactivate_employee,
    inactivate_item,
    InventoryView,
    InventoryViewSet,
    InvoicesView,
    InvoiceView,
    InvoiceViewSet,
    ItemView,
    ItemViewSet,
    LogoutViewSet,
    OrderApprovePurchase,
    OrderRequestView,
    OrderRequestFullView,
    OrderRequestViewSet,
    OrderRequestViewSet2,
    OrderSavePriceToItem,
    OrderStatusListViewSet,
    PaginatedIItemViewSet,
    PaginatedItemInvoiceView,
    PaginatedItemViewSet,
    PaymentView,
    PaymentViewSet,
    PermissionGroupView,
    PermissionsView,
    PermissionsViewSet,
    ProductStockViewSet,
    ProductVariantView,
    ProductVariantViewSet,
    ProductView,
    ProductViewSet,
    ProviderView,
    ProviderViewSet,
    ProvinceCityView,
    ProvinceViewSet,
    PurchaseAditionalInfoViewSet,
    PurchaseDetailsViewSet,
    PurchaseViewSet,
    reset_password,
    RoleView,
    RoleViewSet,
    self_permissions,
    SequenceView,
    SequenceViewSet,
    StatusView,
    TestAPIView,
    TomasFisicasDetailsViewSet,
    TransactionStatusViewSet,
    UnpaginatedGroupViewSet,
    user_data,
    UserView,
    UserViewSet,
    VariantAttributesViewSet,
    WarehouseView,
    WarehouseViewSet,
    WhLatestTomaFisicaView,
    WhOrderRequestView,
    WhOrderRequestViewSet,
    WhProductInventoryViewSet,
    WhStockViewSet,
    WhTomasFisicasViewSet,
    WhTransactionDetailsViewSet,
    WhStockWithPropsViewSet,
    WhTransactionViewSet,
]
