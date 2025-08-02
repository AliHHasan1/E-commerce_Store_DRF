from rest_framework import viewsets
from rest_framework.response import Response

from product.models.product_models import Product, ProductReview
from product.serializers.product_serializers import ProductSerializer, ProductReviewSerializer
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from product.filters import ProductFilter
from django.db.models import Sum
from rest_framework.decorators import action


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

    ## يعرض أكثر 5 منتجات تم طلبها بناءً على إجمالي الكمية المباعة.
    """url: /api/products/top-ordered/"""

    @action(
        detail=False,
        methods=['get'],
        url_path='top-ordered',
    )
    def top_ordered_products(self, request):
        top_products = Product.objects.annotate(
            total_ordered=Sum('orderitem__quantity')
        ).filter(
            total_ordered__isnull=False  # نتجاهل المنتجات التي لم يتم طلبها أبدًا
        ).order_by(
            '-total_ordered'  #  نرتب المنتجات تنازليًا بناءً على الكمية المباعة
        )[:5]
        serializer = self.get_serializer(top_products, many=True)
        return Response(serializer.data)
