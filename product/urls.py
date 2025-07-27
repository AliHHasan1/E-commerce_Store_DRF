from django.urls import path, include
from rest_framework.routers import DefaultRouter
from product.views.category_views import CategoryViewSet
from product.views.product_views import ProductViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
