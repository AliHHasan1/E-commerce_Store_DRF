from rest_framework import viewsets
from product.models import Product
from product.serializers.product_serializers import ProductSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
