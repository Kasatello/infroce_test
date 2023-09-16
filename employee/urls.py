from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView
)

from employee.views import CreateEmployeeView

urlpatterns = [
    path("register/", CreateEmployeeView.as_view(), name="register"),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

app_name = "employee"
