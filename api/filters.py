import django_filters
from django_filters import rest_framework as filters

from api.models import Product


class ProductFilter(django_filters.FilterSet):
    price_min = filters.NumberFilter(field_name="price", lookup_expr='gte')
    price_max = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category_id = filters.NumberFilter(field_name="category__id",
                                       lookup_expr='exact')
    category = filters.CharFilter(field_name="category__name",
                                  lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['name', 'category_id', 'category', 'price_min', 'price_max',
                  'published']
