from rest_framework.permissions import BasePermission

class PostOnlyPermissions(BasePermission):
    message = "You need to be an admin to post data"
    def has_permission(self, request, view):
        if self.action in ('create', ):
            return True
        return False