from django.contrib import admin

from restaurant.models import Restaurant, Menu, Vote

admin.site.register(Restaurant)
admin.site.register(Menu)
admin.site.register(Vote)
