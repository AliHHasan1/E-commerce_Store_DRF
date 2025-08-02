import pytest
from order.models import Order, OrderItem
from account.models import Account
from product.models import Product

@pytest.mark.django_db
def test_order_total():
    account = Account.objects.create(username="essa", email="essa@site.com")
    product = Product.objects.create(name="Tablet", price=500, stock=20)
    order = Order.objects.create(account=account)
    OrderItem.objects.create(order=order, product=product, quantity=2, price_at_time=500)

    assert order.get_total_price() == 1000
