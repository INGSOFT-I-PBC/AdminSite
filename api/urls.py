""" API Url Configuration
The `urlpatterns` list the URLs to the Views
"""
from django.urls import path, include
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    # path('users'),
]
