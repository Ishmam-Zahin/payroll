from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from django.http import Http404

from employee_app.models import Department
from employee_app.api.serializers import DepartmentSerializer
from user_app.api.permissions import IsAdminUser

class Department_List(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        depts = Department.objects.all()

        serializer = DepartmentSerializer(depts, many = True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = DepartmentSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)

class Department_detail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def getDepartment(self, pk):
        try:
            return Department.objects.get(id = pk)
        except:
            raise Http404
    

    # def get(self, request, pk):
    #     dept = self.getDepartment(pk)
    #     serializer = DepartmentSerializer(dept)

    #     return Response(serializer.data)
    
    def put(self, request, pk):
        dept = self.getDepartment(pk)

        serializer = DepartmentSerializer(dept, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_400_BAD_REQUEST, data=serializer.errors)
    
    def delete(self, request, pk):
        dept = self.getDepartment(pk)

        dept.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})