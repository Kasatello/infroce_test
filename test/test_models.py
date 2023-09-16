import pytest

from rest_framework.test import APIClient

from restaurant.models import Menu, Restaurant, Vote, Employee


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_create_restaurant():
    restaurant = Restaurant.objects.create(
        name="Sample Restaurant", description="A sample restaurant description."
    )

    assert restaurant.name == "Sample Restaurant"
    assert restaurant.description == "A sample restaurant description."
    assert str(restaurant) == "Sample Restaurant"
    assert Restaurant.objects.count() == 1


@pytest.mark.django_db
def test_create_menu():
    restaurant = Restaurant.objects.create(
        name="Sample Restaurant", description="A sample restaurant description."
    )
    menu = Menu.objects.create(dishes="Sample Dish", price=10.99, restaurant=restaurant)

    assert menu.dishes == "Sample Dish"
    assert menu.price == 10.99
    assert str(menu) == "Today's menu in Sample Restaurant"


@pytest.fixture
def sample_data():
    restaurant = Restaurant.objects.create(
        name="Sample Restaurant", description="A sample restaurant description."
    )
    menu = Menu.objects.create(dishes="Sample Dish", price=10.99, restaurant=restaurant)
    user = Employee.objects.create(
        username="sample_user",
    )
    return {"menu": menu, "user": user}


@pytest.mark.django_db
def test_create_vote(sample_data):
    vote = Vote.objects.create(
        user=sample_data["user"], menu=sample_data["menu"], rating=4.5
    )

    assert vote.user == sample_data["user"]
    assert vote.menu == sample_data["menu"]
    assert vote.rating == 4.5
