from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from ..models.orderitem_models import OrderItem
from ..serializers.orderitem_serializers import OrderItemSerializer


class OrderItemViewSet(viewsets.ModelViewSet):
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return OrderItem.objects.all()
        return OrderItem.objects.filter(order__customer__user=user)
