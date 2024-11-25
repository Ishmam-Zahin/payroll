from django.db import models

from employee_app.models import Department

genderChoices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
]
relegionChoices = [
    ('islam', 'Islam'),
    ('hindu', 'Hindu'),
    ('christian', 'Christian'),
    ('other', 'Other'),
]
class Employee(models.Model):
    id = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=genderChoices)
    employee_type = models.CharField(max_length=50)
    relegion = models.CharField(max_length=10, choices=relegionChoices)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=100)
    job_grade = models.CharField(max_length=20)
    basic_pay = models.IntegerField()
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='employees')
    on_leave = models.BooleanField(default=False)
    skip_loan = models.BooleanField(default=False)
    payroll = models.BooleanField(default=True)
    image_url = models.CharField(max_length=500, null=True, default=None, blank=True)

    def __str__(self):
        return self.first_name +' '+ self.last_name

