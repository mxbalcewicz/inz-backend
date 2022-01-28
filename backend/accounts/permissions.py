from rest_framework.permissions import BasePermission

STAFF_METHODS = ['GET']

class CheckDeanOrStaffPermission(BasePermission):
    """
    Custom permission checking account status and views allowed for account type
    """
    def has_permission(self, request, view):
        if request.user.is_superuser:
            return True
        if request.user.is_dean:
            return True
        if request.user.is_staff:
            if request.method in STAFF_METHODS:
                return True
            else:
                return False