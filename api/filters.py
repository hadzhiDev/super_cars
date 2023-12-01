from django_filters import rest_framework as filters

from core.models import Car


class CarFilter(filters.FilterSet):
    from_price = filters.NumberFilter(field_name='price', lookup_expr='gte')
    to_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    created_at = filters.DateRangeFilter()

    class Meta:
        model = Car
        fields = ('category', 'owner', 'is_published',)