from django.contrib import admin
from .models import Department, MyUser

# Register your models here.
admin.site.register(Department)
admin.site.register(MyUser)