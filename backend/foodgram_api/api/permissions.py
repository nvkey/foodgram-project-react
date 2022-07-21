from rest_framework import permissions

import users.constants as cnst


class StaffAccessPermissionOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        if hasattr(request.user, cnst.ATTR_ROLE):
            return request.user.role == cnst.ROLE_ADMIN
        return False

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        if hasattr(request.user, cnst.ATTR_ROLE):
            return request.user.role == cnst.ROLE_ADMIN
        return False


class AuthorOrStaffAccessPermissionOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS or request.user.is_superuser:
            return True
        if hasattr(request.user, cnst.ATTR_ROLE):
            return obj.author == request.user or request.user.role == cnst.ROLE_ADMIN
        return False
