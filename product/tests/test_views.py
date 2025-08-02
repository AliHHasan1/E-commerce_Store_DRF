import pytest
from rest_framework.test import APIClient
from product.models import Product

@pytest.mark.django_db
def test_product_list_api():
    Product.objects.create(name="Screen", price=300, stock=10)
    client = APIClient()
    response = client.get("/api/products/")
    assert response.status_code == 200
    assert len(response.data) > 0
