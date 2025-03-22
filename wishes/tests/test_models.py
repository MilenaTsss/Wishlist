import pytest
from django.contrib.auth import get_user_model
from wishes.models import Wish

User = get_user_model()

@pytest.mark.django_db
def test_create_wish():
    user = User.objects.create_user(username="john", password="pass123")
    wish = Wish.objects.create(
        user=user,
        title="New iPhone",
        description="Want the latest iPhone",
        url="https://apple.com/iphone",
        price=999.99,
    )

    assert wish.title == "New iPhone"
    assert wish.user == user
    assert wish.is_reserved is False
    assert wish.is_active is True
    assert wish.created_at is not None
    assert wish.updated_at is not None


@pytest.mark.django_db
def test_reserve_wish():
    owner = User.objects.create_user(username="owner", password="pass123")
    reserver = User.objects.create_user(username="reserver", password="pass456")

    wish = Wish.objects.create(
        user=owner,
        title="PlayStation 5",
        is_reserved=True,
        reserved_by=reserver,
    )

    assert wish.is_reserved is True
    assert wish.reserved_by == reserver


@pytest.mark.django_db
def test_deactivate_wish():
    user = User.objects.create_user(username="john", password="pass123")
    wish = Wish.objects.create(user=user, title="Trip to Japan")

    wish.is_active = False
    wish.save()

    assert not wish.is_active


@pytest.mark.django_db
def test_string_representation():
    user = User.objects.create_user(username="john", password="pass123")
    wish = Wish.objects.create(user=user, title="New Bike")

    assert str(wish) == "New Bike"