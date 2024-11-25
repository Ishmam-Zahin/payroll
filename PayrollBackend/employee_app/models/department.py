from django.db import models

# Create your models here.
class Department(models.Model):
    id = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=200)
    code_name = models.CharField(max_length=10)


    def __str__(self):
        return self.code_name
