from rest_framework.permissions import BasePermission

class IsAdmin(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == "admin"

class IsLawyer(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'lawyer'

class IsCustomer(BasePermission):

    def has_permission(self, request, view):
        return request.user.user_type == 'customer'