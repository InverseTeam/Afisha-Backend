from rest_framework import permissions


class IsManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
            if request.user.is_authenticated:
                if request.method in permissions.SAFE_METHODS:
                    return True

                return request.user.role.role_type == 'manager'

            return False

class IsArtistManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_authenticated:
            if request.method in permissions.SAFE_METHODS:
                return True

            return request.user.id == obj.manager.id

        return False