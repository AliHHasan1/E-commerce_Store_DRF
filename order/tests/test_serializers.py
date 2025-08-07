import pytest
from order.serializers.order_serializers import OrderItemSerializer
from product.models import Product
from order.models import Order
from account.models import Customer
from django.contrib.auth import get_user_model

User = get_user_model()

@pytest.mark.django_db
def test_order_item_serializer_validation():
    product = Product.objects.create(name="Mouse", price=50, stock_quantity=10, is_available=True)
    data = {"product": product, "quantity": 5}
    serializer = OrderItemSerializer(data=data)
    assert serializer.is_valid()

@pytest.mark.django_db
def test_order_item_serializer_invalid_stock():
    product = Product.objects.create(name="Mouse", price=50, stock_quantity=2, is_available=True)
    data = {"product": product, "quantity": 5}
    serializer = OrderItemSerializer(data=data)
    assert not serializer.is_valid()
    assert "المخزون غير كافٍ" in str(serializer.errors)
