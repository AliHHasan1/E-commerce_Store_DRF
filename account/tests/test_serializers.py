import pytest
from account.models import Account
from account.serializers import AccountSerializer

@pytest.mark.django_db
def test_account_serializer():
    acc = Account.objects.create(username="essa", email="essa@example.com")
    serializer = AccountSerializer(acc)
    data = serializer.data
    assert data["email"] == "essa@example.com"
