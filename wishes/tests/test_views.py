import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from wishes.models import Wish

User = get_user_model()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def auth_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
def wish(user):
    return Wish.objects.create(user=user, title="Test Wish", price=123.45)


@pytest.mark.django_db
def test_create_wish(auth_client):
    data = {
        "title": "New Camera",
        "description": "Want for travel",
        "price": "299.99",
        "url": "https://example.com/camera",
    }
    response = auth_client.post("/api/wishes/", data)
    assert response.status_code == 201
    assert response.data["title"] == data["title"]


@pytest.mark.django_db
def test_get_all_wishes(auth_client, wish):
    response = auth_client.get("/api/wishes/")
    assert response.status_code == 200
    assert len(response.data) == 1
    assert response.data[0]["title"] == "Test Wish"


@pytest.mark.django_db
def test_get_single_wish(auth_client, wish):
    response = auth_client.get(f"/api/wishes/{wish.id}/")
    assert response.status_code == 200
    assert response.data["title"] == "Test Wish"


@pytest.mark.django_db
def test_update_wish_put(auth_client, wish):
    data = {
        "title": "Updated Title",
        "description": wish.description,
        "price": "150.00",
        "url": wish.url,
        "is_reserved": wish.is_reserved,
        "is_active": wish.is_active,
    }
    response = auth_client.put(f"/api/wishes/{wish.id}/", data)
    assert response.status_code == 200
    assert response.data["title"] == "Updated Title"
    assert float(response.data["price"]) == 150.00


@pytest.mark.django_db
def test_update_wish_patch(auth_client, wish):
    response = auth_client.patch(f"/api/wishes/{wish.id}/", {"title": "Patched Title"})
    assert response.status_code == 200
    assert response.data["title"] == "Patched Title"


@pytest.mark.django_db
def test_delete_wish(auth_client, wish):
    response = auth_client.delete(f"/api/wishes/{wish.id}/")
    assert response.status_code == 204
    assert Wish.objects.count() == 0
