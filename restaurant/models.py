from django.db import models


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()


class Menu(models.Model):
    dishes = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.IntegerField()
    date = models.DateField(auto_now=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )
