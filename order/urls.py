from django.urls import path, include
from rest_framework.routers import DefaultRouter
from order.views.order_views import OrderItemViewSet , OrderViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('', include(router.urls)),
]
