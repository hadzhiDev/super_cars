from django.urls import path, include

import api.views
from . import views

from rest_framework.routers import DefaultRouter
from .yasg import urlpatterns as url_doc

router = DefaultRouter()
router.register('cars', views.CarViewSet)
router.register('car-brands', views.CarBrandViewSet)
router.register('car-image', views.CarImageViewSet)
router.register('car-attribute', views.CarAttributeViewSet)
router.register('categories', views.CategoryViewSet)

urlpatterns = [
    path('auth/', include('api.auth.urls')),

    path('', include(router.urls))
]

urlpatterns += url_doc
