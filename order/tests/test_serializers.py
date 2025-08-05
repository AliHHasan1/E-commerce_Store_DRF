import pytest
from order.models import Order
from order.serializers import OrderSerializer
from account.models import Customer

@pytest.mark.django_db
def test_order_serializer_fields():
    account = Account.objects.create(username="essa", email="e@e.com")
    order = Order.objects.create(account=account, status="pending")
    serializer = OrderSerializer(order)
    data = serializer.data
    assert data["status"] == "pending"
