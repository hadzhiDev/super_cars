from rest_framework.generics import get_object_or_404
from rest_framework.permissions import BasePermission, SAFE_METHODS

from core.models import Car


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        car = get_object_or_404(Car, id=view.kwargs['id'])

        return car.owner == request.user or request.user.is_superuser


class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):

        return request.user.is_superuser


class IsOwnerForCar(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj.car.owner or request.user.is_superuser


class IsSuperAdminOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in SAFE_METHODS or
            request.user.is_superuser
        )