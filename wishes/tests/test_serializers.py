import pytest
from django.contrib.auth import get_user_model

from wishes.models import Wish
from wishes.serializers import WishSerializer

User = get_user_model()


@pytest.mark.django_db
def test_wish_serializer_valid_data():
    user = User.objects.create_user(username="john", password="pass123")
    data = {
        "title": "Nintendo Switch",
        "description": "Lite version",
        "url": "https://example.com/switch",
        "price": "299.99",
        "is_reserved": False,
        "is_active": True,
    }

    serializer = WishSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    wish = serializer.save(user=user)

    assert wish.title == data["title"]
    assert wish.user == user
    assert str(wish.price) == data["price"]


@pytest.mark.django_db
def test_wish_serializer_missing_required_field():
    data = {"description": "Missing title", "price": "100.00"}

    serializer = WishSerializer(data=data)
    assert not serializer.is_valid()
    assert "title" in serializer.errors


@pytest.mark.django_db
def test_wish_serializer_output():
    user = User.objects.create_user(username="anna", password="pass123")
    wish = Wish.objects.create(
        user=user,
        title="MacBook Air",
        description="M3 chip",
        url="https://example.com/macbook",
        price=999.99,
        is_reserved=False,
        is_active=True,
    )

    serializer = WishSerializer(wish)
    data = serializer.data

    assert data["title"] == "MacBook Air"
    assert data["description"] == "M3 chip"
    assert data["url"] == "https://example.com/macbook"
    assert float(data["price"]) == 999.99
    assert data["is_reserved"] is False
    assert data["is_active"] is True
    assert "created_at" in data
    assert "updated_at" in data
