""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers

from api import views
from .views import LogoutViewSet, PermissionsView, reset_password, WarehouseView

router = routers.DefaultRouter()
router.register(r"users", views.UserViewSet)
router.register(r"permissions", views.PermissionsViewSet)

urlpatterns = [
    path("list/", include(router.urls)),
    path("logout", LogoutViewSet.as_view(), name="logout"),
    path("auth/me/permissions", PermissionsView.as_view(), name="user-permissions"),
    path("warehouse", WarehouseView.as_view(), name="warehouse-list"),
    path("auth/reset-password", reset_password, name="reset-user-password")
    # path('users'),
]
