from rest_framework import permissions


class IsInvolvedOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return (
            obj.sender == request.user
            or obj.receiver == request.user
            or request.user.is_staff
        )
