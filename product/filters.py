import django_filters
from product.models.product_models import Product
from product.models.category_models import Category


class ProductFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    price_max = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = django_filters.ModelChoiceFilter(queryset=Category.objects.filter(is_active=True))

    class Meta:
        model = Product
        fields = ['category', 'price_min', 'price_max', 'name', 'description']
