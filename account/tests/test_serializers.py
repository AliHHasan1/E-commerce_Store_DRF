import pytest
from account.models import Customer
from account.serializers import CustomerSerializer

@pytest.mark.django_db
def test_account_serializer():
    acc = Customer.objects.create(username="essa", email="essa@example.com")
    serializer = CustomerSerializer(acc)
    data = serializer.data
    assert data["email"] == "essa@example.com"
