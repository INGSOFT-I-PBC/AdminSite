#from api.views.authviews import *
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
    PaginatedItemInvoiceView2,

)
from api.views.dashboard import (
    DashboardViewSet,

)
from api.views.creditnote import (
    CreditNoteViewSet
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
    OrderRequestViewSet,
    TomasFisicasDetailsViewSet,
    WarehouseView,
    WarehouseViewSet,
    WhLatestTomaFisicaView,
    WhOrderRequestView,
    WhOrderRequestViewSet,
    WhStockViewSet,
    WhTomasFisicasViewSet,
    WhTransactionDetailsViewSet,
    WhTransactionViewSet,
)

__all__ = [
    CategoryView,
    ClientView,
    create_employee,
    create_order_request,
    create_permission,
    create_prod_variant,
    create_product,
    create_provider,
    create_purchase_status,
    create_user,
    CreateProductView,
    EmployeeView,
    EmployeeViewSet,
    FullClientViewSet,
    FullGenderViewSet,
    FullInventoryViewSet2,
    FullPaymentViewSet,
    FullProductView,
    FullSequenceViewSet,
    FullWarehouseViewSet,
    get_full_order,
    GroupView,
    GroupViewSet,
    InventoryView,
    InventoryViewSet,
    InvoicesView,
    InvoiceView,
    InvoiceViewSet,
    ItemView,
    LogoutViewSet,
    OrderRequestView,
    OrderRequestViewSet,
    OrderStatusListViewSet,
    PaginatedIItemViewSet,
    PaginatedItemInvoiceView,
    PaginatedItemViewSet,
    PermissionsView,
    PermissionsViewSet,
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
    StatusView,
    UnpaginatedGroupViewSet,
    user_data,
    UserView,
    UserViewSet,
    VariantAttributesViewSet,
    WarehouseView,
    WarehouseViewSet,
    WhOrderRequestView,
    WhProductInventoryViewSet,
    ClientViewSet,
    GenderView,
    FullInventoryViewSet,
    ItemViewSet,
    PaymentView,
    PaymentViewSet,
    ProductStockViewSet,
    SequenceView,
    SequenceViewSet,
    WhTransactionViewSet,
    WhStockViewSet,
    WhOrderRequestViewSet,
    WhTomasFisicasViewSet,
    WhLatestTomaFisicaView,
    TomasFisicasDetailsViewSet,
    WhTransactionDetailsViewSet,
    PermissionGroupView,
    activate_employee,
    activate_item,
    activate_user,
    inactivate_employee,
    inactivate_item,
    find_item,
    get_item_properties,
    create_role,
    FullProvinceViewSet,
    CreateTestView,
    TestAPIView,
    CreditNoteViewSet,
]
