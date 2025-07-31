from rest_framework import viewsets
from product.models.product_models import Product,ProductReview
from product.serializers.product_serializers import ProductSerializer,ProductReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import permissions
from product.filters import ProductFilter

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_available=True)
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    
    
class ProductReviewViewSet(viewsets.ModelViewSet):
    queryset = ProductReview.objects.all()
    serializer_class = ProductReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
