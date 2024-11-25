from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.http import Http404

from employee_app.models import Employee
from employee_app.api.serializers import CustomComponentSerializer


class CustomComponent_List(APIView):
    def getEmployee(self, pk):
        try:
            return Employee.objects.get(id = pk)
        except:
            raise Http404

    def get(self, request, pk):
        employee  = self.getEmployee(pk)
        components = employee.customComponents.all()
        serializer = CustomComponentSerializer(components, many = True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = CustomComponentSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data = serializer.errors)