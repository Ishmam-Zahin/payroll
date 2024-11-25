from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User

from employee_app.models import Department

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, user_name = None, department = None, password = None):
        if user_name is None or password is None:
            return None
        
        user = self.model(user_name = user_name, department = department)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, user_name, password=None):
        user = self.create_user(user_name=user_name, password=password)
        user.is_admin = True
        user.save()
        return user

class MyUser(AbstractBaseUser):
    user_name = models.CharField(max_length=100, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, default=None)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = MyUserManager()
    USERNAME_FIELD = 'user_name'

    def __str__(self):
        return self.user_name
    
    def has_perm(self, perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin