from rest_framework import serializers

from payroll_app.models import Payslip

class PayslipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payslip
        fields = '__all__'