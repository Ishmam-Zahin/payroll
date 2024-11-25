from django.db import models

type_choices = [
    ('compensation', 'Compensation'),
    ('deduction', 'Deduction'),
]

gender_choices = [
    ('male', 'Male'),
    ('female', 'Female'),
    ('other', 'Other'),
    ('all', 'All'),
]

class GlobalComponent(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    component_type = models.CharField(max_length=50, choices=type_choices)

    def __str__(self):
        return self.name

class GlobalComponentConditions(models.Model):
    id = models.AutoField(primary_key=True)
    global_component = models.ForeignKey(GlobalComponent, on_delete=models.CASCADE, related_name='globalConditions')
    min_money = models.IntegerField()
    max_money = models.IntegerField()
    gender = models.CharField(max_length=20, choices=gender_choices)
    amount = models.CharField(max_length=10)
    min_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.global_component.name + ' Condition'