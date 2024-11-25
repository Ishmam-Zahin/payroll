from django.db import models

from employee_app.models import Employee, Department

# Create your models here.
class Payslip(models.Model):
    id = models.AutoField(primary_key=True)
    employee_id = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='payslips')
    name = models.CharField(max_length=200)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='dptPayslips')
    department_name = models.CharField(max_length=200)
    from_date = models.DateField()
    to_date = models.DateField()
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=20, default='pending')
    main_payscale = models.IntegerField()
    final_amount = models.IntegerField()
    description = models.JSONField()

    def __str__(self):
        return self.name + '-' + str(self.date)