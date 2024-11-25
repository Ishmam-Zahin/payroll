from django.contrib.auth.backends import BaseBackend, ModelBackend

from .models import MyUser

class MyBackend(BaseBackend):
    def authenticate(self, request, user_name = None, password = None, **kwargs):
        if user_name is None or password is None:
            return None
        try:
            user = MyUser.objects.get(user_name = user_name)
            if not user.check_password(password):
                return None
            return user
        except:
            return None
    
    def get_user(self, user_id):
        try:
            user = MyUser.objects.get(pk = user_id)
            return user
        except:
            return None