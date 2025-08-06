from rest_framework.routers import DefaultRouter
from .views.orderitem_views import OrderItemViewSet
from .views.order_views import OrderViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'order-items', OrderItemViewSet, basename='orderitem')
router.register(r'orders', OrderViewSet, basename='order')
urlpatterns = [
    path('', include(router.urls)),
]