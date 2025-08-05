import pytest
from rest_framework.test import APIClient
from account.models import Customer

@pytest.mark.django_db
def test_order_create_api():
    account = Customer.objects.create(username="essa", email="e@e.com")
    client = APIClient()
    response = client.post("/api/orders/", {
        "account": account.id,
        "status": "pending"
    })
    assert response.status_code == 201
