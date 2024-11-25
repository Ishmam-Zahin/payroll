from rest_framework import serializers

from user_app.models import MyUser

class MyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = '__all__'
    
    def create(self, validatedData):
        user_name = validatedData['user_name']
        department = validatedData['department']
        password = validatedData['password']

        user = MyUser.objects.create_user(user_name = user_name, department = department, password = password)

        return user

class MyUserViewSerializer(MyUserSerializer):
    department = serializers.StringRelatedField()