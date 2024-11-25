from rest_framework.authtoken.views import obtain_auth_token

from django.urls import path

from . import views

urlpatterns = [
    path('account/list/', views.MyUser_List.as_view()),
    path('account/login/', views.MyUser_Login.as_view()),
    path('account/logout/', views.MyUser_Logout.as_view()),
    path('account/detail/<int:pk>/', views.MyUser_Detail.as_view()),
]