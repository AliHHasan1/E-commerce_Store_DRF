import pytest
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from account.models import Customer
from product.models import Product

User = get_user_model()

@pytest.mark.django_db
def test_create_order_success():
    user = User.objects.create_user(username="essa", password="pass123", role="customer")
    Customer.objects.create(user=user, phone="0999999999")
    product = Product.objects.create(name="Laptop", price=1000, stock_quantity=5, is_available=True)

    client = APIClient()
    client.force_authenticate(user=user)

    response = client.post("/orders/", {
        "customer": user.customer.id,
        "items": [{"product_id": product.id, "quantity": 2}]
    }, format="json")

    assert response.status_code == 201
    assert response.data["total_amount"] == 2000

@pytest.mark.django_db
def test_order_status_update_by_admin():
    admin = User.objects.create_user(username="admin", password="adminpass", role="admin", is_superuser=True)
    Customer.objects.create(user=admin, phone="0900000000")
    product = Product.objects.create(name="Phone", price=500, stock_quantity=10, is_available=True)

    client = APIClient()
    client.force_authenticate(user=admin)

    response = client.post("/orders/", {
        "customer": admin.customer.id,
        "items": [{"product_id": product.id, "quantity": 1}]
    }, format="json")
    order_id = response.data["id"]

    response = client.put(f"/orders/{order_id}/status/", {"status": "confirmed"}, format="json")
    assert response.status_code == 200
    assert response.data["status"] == "confirmed"
