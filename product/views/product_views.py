from rest_framework import viewsets
from product.models import Product
from product.serializers.product_serializers import ProductSerializer
from django_filters.rest_framework import DjangoFilterBackend 

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend] 
    filterset_fields = ['name', 'description'] 


