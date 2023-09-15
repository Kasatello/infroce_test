from django.db import models

from employee.models import Employee


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.name


class Menu(models.Model):
    dishes = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    rating = models.IntegerField()
    date = models.DateField(auto_now=True)
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="menus"
    )


class Rating(models.Model):
    user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="ratings"
    )
    menu = models.ForeignKey(
        Menu, on_delete=models.CASCADE, related_name="ratings"
    )
    rating = models.DecimalField(max_digits=2, decimal_places=1)
