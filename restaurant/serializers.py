from rest_framework import serializers

from restaurant.models import Restaurant, Menu, Vote


class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = "__all__"


class VoteSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Vote
        fields = ("rating", "menu", "user")


class MenuSerializer(serializers.ModelSerializer):
    votes = VoteSerializer(many=True, read_only=True, source='vote_set')

    class Meta:
        model = Menu
        fields = "__all__"
