import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name='productcategory__category__title',
        lookup_expr='iexact',  # case-insensitive exact match
        label='Category Title'
    )

    class Meta:
        model = Product
        fields = ['category']
