from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token

from django.contrib.auth import authenticate
from django.http import Http404

from user_app.models import MyUser
from .serializers import MyUserSerializer, MyUserViewSerializer
from .permissions import IsAdminUser


class MyUser_Login(APIView):
    def post(self, request):
        user = authenticate(request, user_name = request.data['user_name'], password = request.data['password'])

        if user is None:
            return Response(status = status.HTTP_406_NOT_ACCEPTABLE, data = {'message': 'invalid credentials'})
        
        (token, auth) = Token.objects.get_or_create(user = user)

        if user.department is None:
            department = 'center'
        else:
            department = user.department.code_name


        return Response({'message': 'login successful.', 'token': token.key, 'name': user.user_name, 'department': department})
    
class MyUser_Logout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'logout successful!'})


class MyUser_List(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get(self, request):
        users = MyUser.objects.all()
        serializer = MyUserViewSerializer(users, many = True)

        return Response(serializer.data)
    
    def post(self, request):
        serializer = MyUserSerializer(data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(status = status.HTTP_400_BAD_REQUEST, data = serializer.errors)

class MyUser_Detail(APIView):
    permission_classes = [IsAuthenticated, IsAdminUser]
    
    def getUser(self, pk):
        try:
            return MyUser.objects.get(id = pk)
        except:
            raise Http404
        
    def delete(self, request, pk):
        user = self.getUser(pk)
        user.delete()

        return Response(status=status.HTTP_200_OK, data={'message': 'deleted'})