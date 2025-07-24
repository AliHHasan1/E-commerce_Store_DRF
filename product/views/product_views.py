from rest_framework import viewsets
from product.models import Product
from product.serializers.product_serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend 

from product.filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter