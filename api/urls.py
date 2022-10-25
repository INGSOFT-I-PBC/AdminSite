""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views
from .views import *
from .views.itemviews import ItemView
from .views.orders import OrderRequestView
from .views.warehouse import *
from .views.clientview import *

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses/all", views.FullWarehouseViewSet)
router.register(r"clients/all", views.FullClientViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"items", views.PaginatedItemViewSet, "paginatedItemVS")


urlpatterns = [
    # List return paths
    path("list/", include(router.urls)),
    # Auth paths
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", PermissionsView.as_view(), name="user-permissions"),
    path("auth/me", user_data, name="user-data"),
    # Path for models
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    path("warehouse/order", WhOrderRequestView.as_view(), name="wh-orders"),
    path("warehouse/inventory", WhInventoryView.as_view(), name="wh-inventory"),
    path("warehouse/purchase-order", WhPurchaseView.as_view(), name="wh-purchase"),
    path("warehouse/movements", WhTransactionView.as_view(), name="wh-movements"),
    path("items", ItemView.as_view(), name="item-list"),
    path("items/<int:pk>", ItemView.as_view(), name="item_process"),
    path("category", CategoryView.as_view(), name="category-list"),
    path("category/<int:id>", CategoryView.as_view(), name="category_process"),
    path("inventory", InventoryView.as_view(), name="inventory-list"),
    path("inventory/<int:pk>", InventoryView.as_view(), name="inventory_process"),
    path("item/<int:id>", views.find_item, name="item"),
    path("item/<int:id>/properties", views.get_item_properties),
    path("order", OrderRequestView.as_view()),
    path("auth/reset-password", reset_password, name="reset-user-password")
    # path('users'),
]
