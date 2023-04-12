from django.test import TestCase
from django.contrib.auth import get_user_model
import pytest
User = get_user_model()


# Create your tests here.

@pytest.mark.django_db
def test_create_user():
    user = User.objects.create_user(
        username = "Dave",
        email = "test@test.com",
        password = "testpass123",
    )

    assert user.username == "Dave"
    assert user.email == "test@test.com"
    assert user.is_staff == False
    assert user.is_superuser == False


@pytest.mark.django_db
def test_create_superuser():
    user = User.objects.create_superuser(
        username = "SuperDave",
        email = "supertest@test.com",
        password = "testpass123",
    )

    assert user.username == "SuperDave"
    assert user.email == "supertest@test.com"
    assert user.is_staff == True
    assert user.is_superuser == True


