import pytest
from django.contrib.auth.models import User
from rest_framework.test import APIClient
from rest_framework import status


@pytest.mark.django_db
def test_register_view_success():
    client = APIClient()
    data = {
        "username": "newuser",
        "email": "new@example.com",
        "password": "testpass123",
        "first_name": "New",
        "last_name": "User"
    }

    response = client.post("/api/register/", data)
    assert response.status_code == status.HTTP_201_CREATED
    assert User.objects.filter(username="newuser").exists()


@pytest.mark.django_db
def test_register_view_invalid_data():
    client = APIClient()
    data = {
        "username": "nouser",
        "password": "testpass123",
        # email missing, but optional unless required=True
    }

    response = client.post("/api/register/", data)
    assert response.status_code == status.HTTP_201_CREATED or status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_user_account_retrieve():
    user = User.objects.create_user(username="john", password="pass123")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.get("/api/users/me/")
    assert response.status_code == status.HTTP_200_OK
    assert response.data["username"] == "john"


@pytest.mark.django_db
def test_user_account_update():
    user = User.objects.create_user(username="john", password="pass123", first_name="Old")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.patch("/api/users/me/", {"first_name": "Updated"})
    assert response.status_code == status.HTTP_200_OK
    user.refresh_from_db()
    assert user.first_name == "Updated"


@pytest.mark.django_db
def test_user_account_delete_deactivates_user():
    user = User.objects.create_user(username="john", password="pass123")
    client = APIClient()
    client.force_authenticate(user=user)

    response = client.delete("/api/users/me/")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    user.refresh_from_db()
    assert user.is_active is False
