from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth import login

from .models import MyUser, Department
# Create your views here.

def testView(request):
    # # dept = Department.objects.get(pk=1)
    # # user = MyUser.objects.create_user(email = 'afc@gmail.com', department = dept, password = '1234')
    # # # print(user)
    # # user = authenticate(request, email = 'abc@gmail.com', password = '1234')
    # # # print(user)
    # # if user is not None:
    # #     login(request, user=user)
    # if not request.user.is_authenticated:
    #     return HttpResponse('not authorized')
    
    # print(request.user)
    # print(request.user.is_admin)
    return HttpResponse('hello word')