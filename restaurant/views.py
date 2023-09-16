import random
from datetime import date

from django.db.models import Avg, Count
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from restaurant.models import Restaurant, Menu, Vote
from restaurant.serializers import RestaurantSerializer, MenuSerializer, VoteSerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer
    # permission_classes = [IsAuthenticated]


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all()
    serializer_class = MenuSerializer
    # permission_classes = [IsAuthenticated]


class GenerateMenu(views.APIView):
    # permission_classes = [IsAdminUser]

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
    # permission_classes = [IsAuthenticated]

    def get(self, request, menu_id):
        menu_obj = get_object_or_404(Menu, pk=menu_id)
        menu_results = (
            Vote.objects.filter(menu=menu_obj)
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


class VoteViewSet(viewsets.ModelViewSet):
    queryset = Vote.objects.all()
    serializer_class = VoteSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=["POST"])
    def vote(self, request, pk=None):
        menu_id = request.data.get("menu_id")

        try:
            menu = Menu.objects.get(pk=menu_id)
        except Menu.DoesNotExist:
            return Response({"detail": "Menu not found"}, status=status.HTTP_404_NOT_FOUND)

        vote = Vote(menu=menu, user=request.user)

        rating = request.data.get("rating")

        if rating is None:
            return Response({"detail": "Rating is required"}, status=status.HTTP_400_BAD_REQUEST)

        vote.rating = rating
        vote.save()

        serializer = VoteSerializer(vote)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

