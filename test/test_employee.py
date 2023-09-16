import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def employee_user():
    return User.objects.create_user(
        username="testuser",
        password="testpass",
    )


@pytest.fixture
def superuser():
    return User.objects.create_superuser(
        username="adminuser",
        password="adminpass",
    )


@pytest.mark.django_db
def test_employee_user_creation(employee_user):
    assert employee_user.username == "testuser"
    assert employee_user.check_password("testpass")


@pytest.mark.django_db
def test_superuser_creation(superuser):
    assert superuser.username == "adminuser"
    assert superuser.check_password("adminpass")
    assert superuser.is_staff is True
    assert superuser.is_superuser is True
