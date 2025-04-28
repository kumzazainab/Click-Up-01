from rest_framework.permissions import BasePermission

class IsAdminOrProjectManager(BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'project manager']


from rest_framework.permissions import BasePermission

class IsAdminCanDelete(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'DELETE':
            return request.user.is_authenticated and request.user.is_staff
        return request.user.is_authenticated
