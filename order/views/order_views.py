from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django_filters.rest_framework import DjangoFilterBackend

from order.models import Order, OrderItem
from order.serializers.order_serializers import (
    OrderSerializer,
    OrderItemSerializer,
    OrderStatusUpdateSerializer
)
from store.permissions import OrderPermissions


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('customer').prefetch_related('items__product')
    serializer_class = OrderSerializer
    permission_classes = [OrderPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['customer', 'status']

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['put'], serializer_class=OrderStatusUpdateSerializer, url_path='status')
    def update_status(self, request, pk=None):
        order = self.get_object()
        if request.user.role not in ['admin', 'seller']:
            raise PermissionDenied("ليس لديك صلاحية تعديل الحالة.")
        serializer = self.get_serializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.select_related('order', 'product')
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return self.queryset
        return self.queryset.filter(order__customer__user=user)
