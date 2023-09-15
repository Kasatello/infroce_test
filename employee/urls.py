from django.urls import path

from employee.views import CreateEmployeeView

urlpatterns = [
    path("register/", CreateEmployeeView.as_view(), name="register")
]

app_name = "employee"
