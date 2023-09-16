import random
from datetime import date

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, views
from rest_framework.response import Response

from restaurant.models import Restaurant, Menu, Rating
from restaurant.serializers import RestaurantSerializer, MenuSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer


class GenerateMenu(views.APIView):
    def post(self, request):
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

    @classmethod
    def get_extra_actions(cls):
        return []


class MenuResult(views.APIView):
    def get(self, request, menu_id):
        menu_obj = get_object_or_404(Menu, pk=menu_id)
        menu_results = (
            Rating.objects.filter(menu=menu_obj)
            .values("menu__dishes")
            .annotate(avg_rating=Avg("rating"))
            .annotate(menus_sold=Count("rating"))
        )
        result = [
            {
                "dishes": item["menu__dishes"],
                "avg_rating": item["avg_rating"],
                "menus_sold": item["menus_sold"]
            }
            for item in menu_results
        ]
        return Response({"menu_results": result}, status=status.HTTP_200_OK)

    @classmethod
    def get_extra_actions(cls):
        return []
