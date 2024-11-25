from django.urls import path
from . import views

urlpatterns = [
    path('department/list/', views.Department_List.as_view()),
    path('department/<int:pk>/', views.Department_detail.as_view()),
    path('globalComponent/list/', views.GlobalComponent_List.as_view()),
    path('globalComponent/detail/<int:pk>/', views.GlobalComponent_Detail.as_view()),
    path('employee/list/', views.Employee_List.as_view()),
    path('employee/detail/<int:pk>/', views.Employee_Detail.as_view()),
    path('customComponent/list/<int:pk>/', views.CustomComponent_List.as_view()),
]