from rest_framework.permissions import BasePermission


class IsAdminOrSuperUser(BasePermission):
    """Access only for admin or superuser."""

    def has_permission(self, request, view):
        return (hasattr(request.user, 'role')
                and request.user.is_admin
                or request.user.is_superuser)


class IsModerator(BasePermission):
    """Access only for moderators."""

    def has_permission(self, request, view):
        return hasattr(request.user, 'role') and request.user.is_moderator
