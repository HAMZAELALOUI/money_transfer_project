import pytest
from users.models import User


@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(username="testuser", password="testpass123")
    assert user.username == "testuser"
    assert user.is_active
