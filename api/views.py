from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import filters

from django_filters.rest_framework import DjangoFilterBackend

from api.filters import CarFilter
from api.mixins import UltraModelViewSet
from api.paginations import SimpleResultPagination
from api.permissions import IsOwner, IsSuperAdmin, IsOwnerForCar, IsSuperAdminOrReadOnly
from api.serializers import (CategorySerializer, CarSerializer, BrandSerializer, ReadCarSerializer,
                             CreateCarSerializer, CarAttributeSerializer, CarImageSerializer)
from core.models import Category, Car, Brand, CarImage, CarAttribute


class CategoryViewSet(UltraModelViewSet):
    queryset = Category.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = CategorySerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated, IsSuperAdmin,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'destroy': (IsAuthenticated, IsSuperAdmin,),
    }


class CarViewSet(UltraModelViewSet):
    queryset = Car.objects.all()
    serializer_classes = {
        'list': ReadCarSerializer,
        'update': CreateCarSerializer,
        'create': CarSerializer,
        'retrieve': ReadCarSerializer,
    }
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    ordering_fields = ['is_published', 'price']
    search_fields = ['model', 'overview']
    filterset_class = CarFilter
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsOwner,),
        'destroy': (IsAuthenticated, IsOwner,),
    }


class CarBrandViewSet(UltraModelViewSet):
    queryset = Brand.objects.all()
    pagination_class = SimpleResultPagination
    serializer_class = BrandSerializer
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated, IsSuperAdmin,),
        'update': (IsAuthenticated, IsSuperAdmin,),
        'destroy': (IsAuthenticated, IsSuperAdmin,),
    }


class CarAttributeViewSet(UltraModelViewSet):
    queryset = CarAttribute.objects.all()
    serializer_class = CarAttributeSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    search_fields = ['name', 'value']
    filterset_fields = ['car']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsOwnerForCar,),
        'destroy': (IsAuthenticated, IsOwnerForCar,),
    }


class CarImageViewSet(UltraModelViewSet):
    queryset = CarImage.objects.all()
    serializer_class = CarImageSerializer
    pagination_class = SimpleResultPagination
    lookup_field = 'id'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter, DjangoFilterBackend]
    filterset_fields = ['car']
    permission_classes_by_action = {
        'list': (AllowAny,),
        'retrieve': (AllowAny,),
        'create': (IsAuthenticated,),
        'update': (IsAuthenticated, IsOwnerForCar,),
        'destroy': (IsAuthenticated, IsOwnerForCar,),
    }
