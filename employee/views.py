from rest_framework import generics

from employee.serializers import EmployeeRegistrationSerializer


class CreateEmployeeView(generics.CreateAPIView):
    serializer_class = EmployeeRegistrationSerializer
