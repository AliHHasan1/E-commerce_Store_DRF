import pytest
from account.models import Customer

@pytest.mark.django_db
def test_account_creation():
    acc = Customer.objects.create(username="essa", email="essa@example.com")
    assert acc.username == "essa"
