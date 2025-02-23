from rest_framework import permissions

from django.contrib.auth.models import Group

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Tylko właściciel moze edytować swój snippet
    """

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
    
        return obj.owner == request.user