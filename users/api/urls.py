"""Url-path users app."""
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import UserViewSet, create_user_by_email, get_jwt_token

router_v1 = DefaultRouter()

router_v1.register('', UserViewSet)
urlpatterns = [
    path('v1/auth/email/', create_user_by_email),
    path('v1/auth/token/', get_jwt_token),
    path('v1/users/', include(router_v1.urls)),
]
