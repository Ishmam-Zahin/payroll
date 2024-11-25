from django.contrib import admin
from .models import GlobalComponent, GlobalComponentConditions, Employee

# Register your models here.
admin.site.register(GlobalComponent)
admin.site.register(GlobalComponentConditions)
admin.site.register(Employee)
