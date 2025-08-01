import pytest
from product.models import Product

@pytest.mark.django_db
def test_product_creation():
    p = Product.objects.create(name="Mouse", price=75, stock=50)
    assert p.name == "Mouse"
    assert p.price == 75
    assert p.stock == 50
