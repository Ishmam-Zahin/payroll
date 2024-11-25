from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from django.db import transaction
from django.http import Http404

from user_app.api.permissions import IsAdminUser
from employee_app.models import Employee
from employee_app.api.serializers import EmployeeSerializer, EmployeeShortSerializer, EmployeeDetailSerializer
from employee_app.api.permissions import AdminOrSafeMethod

class Employee_List(APIView):
    def get(self, request):
        employees = Employee.objects.all()
        serializer = EmployeeShortSerializer(employees, many=True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = EmployeeSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.data)


class Employee_Detail(APIView):
    def getEmployee(self, pk):
        try:
            return Employee.objects.get(id = pk)
        except:
            raise Http404
    
    def get(self, request, pk):
        employee = self.getEmployee(pk)
        serializer = EmployeeDetailSerializer(employee)

        return Response(serializer.data)
    
    def put(self, request, pk):
        employee = self.getEmployee(pk)
        serializer = EmployeeSerializer(employee, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def delete(self, request, pk):
        employee = self.getEmployee(pk)

        employee.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})