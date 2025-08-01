import pytest
from product.serializers import ProductSerializer
from product.models import Product

@pytest.mark.django_db
def test_product_serializer():
    product = Product.objects.create(name="Keyboard", price=120, stock=30)
    serializer = ProductSerializer(product)
    data = serializer.data
    assert data["name"] == "Keyboard"
    assert data["price"] == 120
