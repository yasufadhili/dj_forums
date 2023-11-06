from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        # Allow read-only (GET) for any user.
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow updates and deletes for the resource's author.
        return obj.author == request.user
