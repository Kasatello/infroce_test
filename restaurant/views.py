import random
from datetime import date

from django.db.models import Avg, Count

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser

from restaurant.models import Restaurant, Menu
from restaurant.serializers import RestaurantSerializer, MenuSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer

    @action(
        methods=["POST"],
        detail=False,
        url_path="generate_menu",
        permission_classes=[IsAdminUser]
    )
    def generate_menu(self, request):
        dishes = ["Pizza", "Sushi", "Borsch", "Caesar", "Vareniky"]
        current_date = date.today()
        menu = Menu.objects.filter(date=current_date).first()

        if not menu:
            select_dish = random.choice(dishes)
            restaurant = Restaurant.objects.first()
            Menu.objects.create(
                date=current_date, dishes=select_dish, restaurant=restaurant
            )
            return Response({"message": "Menu generated successfully"})
        return Response({"message": "Menu already generated"})


    @action(
        method=["GET"],
        detail=False,
        url_path=["menu_results"]
    )
    def menu_result(self, request):
        menu_results = (
            Menu.objects.values("dishes")
            .annotate(avg_rating=Avg("rating__rating"))
            .annotate(menus_sold=Count("rating"))
        )
        result = [
            {
                "dishes": item["dishes"],
                "avg_rating": item["avg_rating"],
                "menus_sold": item["menus_sold"]
            }
            for item in menu_results
        ]
        return Response({"menu_results": result}, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []
