from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("restaurant.urls", namespace="restaurant")),
    path("api/user/", include("employee.urls", namespace="employee")),
]
