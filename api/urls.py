""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenBlacklistView

from api import views
from .views import *
from .views.warehouse import WhOrderRequestView

router = routers.DefaultRouter(trailing_slash=False)
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)
router.register(r"warehouses/order-requests", views.OrderRequestViewSet)
router.register(r"warehouses", views.WarehouseViewSet)

urlpatterns = [
    path("list/", include(router.urls)),
    path("logout", TokenBlacklistView.as_view(), name="logout"),
    path("auth/me/permissions", PermissionsView.as_view(), name="user-permissions"),
    path("auth/me", user_data, name="user-data"),
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    path("warehouse/puchase-order", WhOrderRequestView.as_view(), name="wh-orders"),
    path("auth/reset-password", reset_password, name="reset-user-password")
    # path('users'),
]
