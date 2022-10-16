""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views

from .views import *
from .views.orders import OrderRequestView
from .views.warehouse import WhOrderRequestView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses/all", views.FullWarehouseViewSet)
router.register(r"warehouses", views.WarehouseViewSet)
router.register(r"items/all", views.ItemViewSet, "itemViewSet")
router.register(r"items", views.PaginatedItemViewSet, "paginatedItemVS")
router.register(r"employees", views.EmployeeViewSet, "employeeViewSet")

urlpatterns = [
    # List return paths
    path("list/", include(router.urls)),
    # Auth paths
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", PermissionsView.as_view(), name="user-permissions"),
    path("auth/me", user_data, name="user-data"),
    # Path for models
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
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
    path("auth/reset-password", reset_password, name="reset-user-password"),
]
