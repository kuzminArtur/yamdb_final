from rest_framework import permissions


class IsAdminOrReadOnly(permissions.BasePermission):
    """Permission for actions with an instance of the class for the admin."""

    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or hasattr(request.user, 'role') and request.user.is_admin)


class IsOwnerOrAdminOrModeratorOrReadOnly(permissions.BasePermission):
    """Only the review owner, moderator, or admin can delete or patch."""

    def has_object_permission(self, request, view, object):
        return (request.method in permissions.SAFE_METHODS
                or request.user == object.author
                or request.user.is_admin
                or request.user.is_superuser
                or request.user.is_moderator)
