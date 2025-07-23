from rest_framework.routers import DefaultRouter
from .views.orderitem_views import OrderItemViewSet
from django.urls import path, include


router = DefaultRouter()
router.register(r'order-items', OrderItemViewSet, basename='orderitem')

urlpatterns = [
    path('api/', include(router.urls)),
]