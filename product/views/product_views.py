from rest_framework import viewsets
from product.models import Product
from product.serializers.product_serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend 

from product.filters import ProductFilter
from store.permissions import ProductPermissions


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    permission_classes = [ProductPermissions]

    def perform_create(self, serializer):
        if self.request.user.role == 'seller':
            serializer.save(seller=self.request.user)
        else:
            serializer.save()