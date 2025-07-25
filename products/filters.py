import django_filters
from .models import Product

class ProductFilter(django_filters.FilterSet):
    category = django_filters.NumberFilter(
        field_name='productcategory__category__id',
        label='Category ID'
    )

    class Meta:
        model = Product
        fields = ['category']
