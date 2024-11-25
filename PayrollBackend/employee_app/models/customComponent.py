from django.db import models

from employee_app.models import Employee

type_choices = [
    ['compensation', 'Compensation'],
    ['deduction', 'Deduction'],
]
class CustomComponent(models.Model):
    id = models.AutoField(primary_key=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='customComponents')
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=30, choices=type_choices)
    amount = models.IntegerField()
    dsc = models.TextField()

    def __str__(self):
        return self.name