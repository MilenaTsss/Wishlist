import pytest
from django.contrib.auth.models import User
from users.serializers import (
    RegistrationSerializer,
    UserSerializer,
    UpdateUserSerializer
)


@pytest.mark.django_db
def test_registration_serializer_creates_user():
    data = {
        "username": "testuser",
        "email": "test@example.com",
        "password": "strongpassword123",
        "first_name": "Test",
        "last_name": "User"
    }
    serializer = RegistrationSerializer(data=data)
    assert serializer.is_valid()
    user = serializer.save()
    assert user.username == data["username"]
    assert user.email == data["email"]
    assert user.first_name == data["first_name"]
    assert user.last_name == data["last_name"]
    assert user.check_password(data["password"])


@pytest.mark.django_db
def test_registration_serializer_missing_fields():
    data = {"username": "testuser"}
    serializer = RegistrationSerializer(data=data)
    assert not serializer.is_valid()
    assert "password" in serializer.errors
    assert "email" not in serializer.errors


@pytest.mark.django_db
def test_user_serializer_output():
    user = User.objects.create_user(
        username="john",
        email="john@example.com",
        password="pass1234",
        first_name="John",
        last_name="Doe"
    )
    serializer = UserSerializer(user)
    data = serializer.data
    expected_keys = {"id", "username", "email", "first_name", "last_name", "is_active"}
    assert set(data.keys()) == expected_keys
    assert data["username"] == "john"
    assert data["email"] == "john@example.com"


@pytest.mark.django_db
def test_update_user_serializer():
    user = User.objects.create_user(
        username="jane",
        email="jane@example.com",
        password="pass1234",
        first_name="Old",
        last_name="Name"
    )
    data = {"first_name": "New", "last_name": "User"}
    serializer = UpdateUserSerializer(user, data=data, partial=True)
    assert serializer.is_valid()
    updated_user = serializer.save()
    assert updated_user.first_name == "New"
    assert updated_user.last_name == "User"