from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

from employee.models import Employee


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    dishes = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    date = models.DateField(auto_now=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )

    def __str__(self):
        return f"Today's menu in {self.restaurant.name}"


class Vote(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="votes"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="votes"
    )
    rating = models.DecimalField(
        max_digits=3,
        decimal_places=1,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
