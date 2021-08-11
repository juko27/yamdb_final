from rest_framework import permissions


class IsAuthorOrSuperUser(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        elif obj.author == request.user or \
                request.user.role in ['admin', 'moderator', ]:
            return True
        return False


class IsSuperUser(permissions.BasePermission):

    def has_permission(self, request, view):
        return (
            request.user.is_superuser
            or request.method in permissions.SAFE_METHODS
        )
