from django.contrib.auth import get_user_model
from rest_framework import permissions

User = get_user_model()


class IsAdmin(permissions.BasePermission):

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        elif request.user.role == 'admin' or request.user.is_superuser:
            return True
        return False


class IsModerator(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif request.user.role in ['admin', 'moderator', ] or \
                request.user.is_superuser:
            return True
        return False


class IsUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif request.user.role in ['admin', 'moderator', 'user', ] or \
                request.user.is_superuser:
            return True
        return False
