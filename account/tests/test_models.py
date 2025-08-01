import pytest
from account.models import Account

@pytest.mark.django_db
def test_account_creation():
    acc = Account.objects.create(username="essa", email="essa@example.com")
    assert acc.username == "essa"
