from rest_framework import permissions


class CheckOwnerCreate(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'owner':
            return False
        return True

class CheckReviewUser(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.user.role == 'client':
            return True
        return False



class CheckReviewEdit(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.username

