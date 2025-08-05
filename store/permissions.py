from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_authenticated and request.user.role == 'admin')


class ProductPermissions(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        if request.method == 'POST':
            return request.user and request.user.is_authenticated and request.user.role in ['admin', 'seller']
        return request.user and request.user.is_authenticated and request.user.role in ['admin', 'seller']

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user.role == 'admin':
            return True
        return obj.seller == request.user

class OrderPermissions(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role in ['admin', 'seller']:
            return True
        return obj.seller == request.user

class UserPermissions(BasePermission):

    def has_permission(self, request, view):
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        if view.action in ['retrieve', 'destroy', 'update', 'partial_update']:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if request.user.role == 'admin':
            return True
        return obj == request.user
    
class IsAdminOrSeller(BasePermission):
    """
    Custom permission to allow only 'admin' or 'seller' roles to access.
    """
    def has_permission(self, request, view):
        if request.user.is_authenticated:
            return request.user.role in ['admin', 'seller']
        return False