from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import Register, Verify, UsersCommonViewSet

router = DefaultRouter()

router.register('users',
                UsersCommonViewSet,
                basename='users')
router.register('users/me',
                UsersCommonViewSet,
                basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/email', Register.as_view(), name="auth"),
    path('auth/token', Verify.as_view(), name='token_obtain_pair'),
]
