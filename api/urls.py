""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers
from api import views
from .views import LogoutView, PermissionsView

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('logout', LogoutView.as_view(), name='logout'),
    path('permissions', PermissionsView.as_view(), name='user-permissions'),
    # path('users'),
]
