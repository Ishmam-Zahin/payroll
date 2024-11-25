from rest_framework import serializers

from django.db.models import Q

from employee_app.models import Department, GlobalComponent, GlobalComponentConditions, Employee, CustomComponent

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'

class GlobalComponentConditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlobalComponentConditions
        fields = '__all__'

class GlobalComponentSerializer(serializers.ModelSerializer):
    globalConditions= GlobalComponentConditionSerializer(many = True, read_only = True)
    class Meta:
        model = GlobalComponent
        fields = '__all__'

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = '__all__'

class EmployeeShortSerializer(EmployeeSerializer):
    department = serializers.StringRelatedField()
    class Meta(EmployeeSerializer.Meta):
        fields = ['id', 'first_name', 'last_name', 'image_url', 'department', 'employee_type', 'on_leave', 'email']

class GlobalComponentConditionShortSerializer(GlobalComponentConditionSerializer):
    global_component = serializers.StringRelatedField(read_only = True)
    component_type = serializers.SerializerMethodField(read_only = True)
    class Meta(GlobalComponentConditionSerializer.Meta):
        fields = ['amount', 'min_amount', 'global_component', 'component_type']
    
    def get_component_type(self, obj):
        return obj.global_component.component_type

class EmployeeDetailSerializer(EmployeeSerializer):
    department = DepartmentSerializer(read_only = True)
    globalComponents = serializers.SerializerMethodField(read_only = True)

    def get_globalComponents(self, obj):
        amount = obj.basic_pay
        gender = obj.gender
        components = GlobalComponentConditions.objects.filter(Q(gender = gender) | Q(gender = 'all'),min_money__lte = amount, max_money__gte = amount)
        serializer = GlobalComponentConditionShortSerializer(components, many = True)

        return serializer.data


class CustomComponentSerializer(serializers.ModelSerializer):
    class Model:
        model = CustomComponent
        fields = '__all__'

