
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from product.models import Category
from product.serializers.category_serializers import CategorySerializer
from product.serializers.product_serializers import ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @action(detail=True, methods=['get'])
    def products(self, request, pk=None):
        category = self.get_object()
        products = category.products.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)



