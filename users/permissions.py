from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем"""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


class IsUser(permissions.BasePermission):
    """Проверяет, является ли пользователь владельцем профиля"""

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
