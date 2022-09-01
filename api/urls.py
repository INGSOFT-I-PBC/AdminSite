""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers

from api import views
from .views import LogoutView, PermissionsView, reset_password, WarehouseView

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)

urlpatterns = [
    path("view-sets/", include(router.urls)),
    path("logout", LogoutView.as_view(), name="logout"),
    path("permissions", PermissionsView.as_view(), name="user-permissions"),
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    path("auth/reset-password", reset_password, name="reset-user-password")
    # path('users'),
]
