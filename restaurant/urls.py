from django.urls import path, include
from rest_framework import routers

from restaurant.views import (
    RestaurantViewSet,
    MenuViewSet,
    GenerateMenu,
    MenuResult,
    VoteViewSet,
)

router = routers.DefaultRouter()
router.register("restaurants", RestaurantViewSet)
router.register("menus", MenuViewSet)
router.register("votes", VoteViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("generate_menu/", GenerateMenu.as_view(), name="generate_menu"),
    path("menu_result/<int:menu_id>", MenuResult.as_view(), name="menu_result"),
]

app_name = "restaurant"
