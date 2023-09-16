import pytest
from datetime import date
from decimal import Decimal
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from restaurant.models import Restaurant, Menu, Vote
from employee.models import Employee

from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def admin_user():
    return Employee.objects.create_superuser(username="admin", password="adminpass")


@pytest.fixture
def user_instance():
    return User.objects.create_user(username="testuser", password="testpass")


@pytest.fixture
def employee_user():
    return Employee.objects.create_user(username="employee", password="employeepass")


@pytest.fixture
def restaurant_instance():
    return Restaurant.objects.create(name="Test Restaurant", description="Description")


@pytest.fixture
def menu_instance(restaurant_instance):
    return Menu.objects.create(
        dishes="Test Dish",
        price=10.99,
        date=date.today(),
        restaurant=restaurant_instance,
    )


@pytest.fixture
def vote_instance(employee_user, menu_instance):
    return Vote.objects.create(
        user=employee_user,
        menu=menu_instance,
        rating=Decimal("4.0"),
    )


@pytest.mark.django_db
def test_generate_menu_view_already_generated(api_client, admin_user, menu_instance):
    api_client.force_authenticate(user=admin_user)
    url = reverse("restaurant:generate_menu")
    response = api_client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {"message": "Menu already generated"}


@pytest.mark.django_db
def test_vote_view_missing_rating(api_client, employee_user, menu_instance):
    api_client.force_authenticate(user=employee_user)
    url = reverse("restaurant:vote-list")
    data = {"menu_id": menu_instance.id}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_vote_menu_duplicate(api_client, employee_user, vote_instance):
    api_client.force_authenticate(user=employee_user)
    url = reverse("restaurant:vote-list")
    data = {"menu_id": vote_instance.menu.id, "rating": 4.0}
    response = api_client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.django_db
def test_menu_results_view(api_client, employee_user, menu_instance, vote_instance):
    api_client.force_authenticate(user=employee_user)
    url = reverse("restaurant:menu_result", args=[menu_instance.id])
    response = api_client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data == {
        "menu_results": [
            {"dishes": "Test Dish", "avg_rating": Decimal("4.0"), "menus_sold": 1}
        ]
    }
