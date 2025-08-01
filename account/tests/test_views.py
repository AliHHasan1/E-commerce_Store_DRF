import pytest
from rest_framework.test import APIClient

@pytest.mark.django_db
def test_register_view():
    client = APIClient()
    response = client.post("/api/account/register/", {
        "username": "essa",
        "password": "secret123",
        "email": "essa@example.com"
    })
    assert response.status_code == 201
