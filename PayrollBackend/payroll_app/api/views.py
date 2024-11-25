from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


from django.db.models import Q, Sum
from django.db.models.functions import ExtractMonth

from employee_app.models import Employee, GlobalComponent, GlobalComponentConditions
from payroll_app.models import Payslip
from .serializers import PayslipSerializer

from datetime import datetime



class Payslip_List(APIView):
    permission_classes = [IsAuthenticated]

    def calculate_tax(self, employee, payslip, taxFromDate, taxToDate):
        yearIncome = employee.payslips.filter(from_date__gte = taxFromDate, to_date__lte = taxToDate).aggregate(total=Sum('final_amount'))['total']

        if yearIncome == None:
            yearIncome = payslip['final_amount']
        else:
            yearIncome += payslip['final_amount']

        if employee.gender == 'male' and yearIncome >= 350000:
            payslip['description']['deductions'].append({'name': 'Income Tax', 'amount': 4000})
            payslip['final_amount'] -= 4000
        elif employee.gender == 'female' and yearIncome >= 400000:
            payslip['description']['deductions'].append({'name': 'Income Tax', 'amount': 4000})
            payslip['final_amount'] -= 4000
        else:
            payslip['description']['deductions'].append({'name': 'Income Tax', 'amount': 0})

    def calculate_payroll(self, employee, data):
        fromDate = datetime.strptime(data['from_date'], '%Y-%m-%d').date()
        toDate = datetime.strptime(data['to_date'], '%Y-%m-%d').date()

        salary = employee.basic_pay
        gender  =employee.gender
        final_pay = salary

        payslip = {
            'employee_id': employee.id,
            'name': (employee.first_name+employee.last_name),
            'department': employee.department.id,
            'department_name': employee.department.full_name,
            'from_date': fromDate,
            'to_date': toDate,
            'main_payscale': salary,
            'final_amount': final_pay,
            'description': {
                'compensations' : [],
                'deductions': [],
            },
        }

        conditions = GlobalComponentConditions.objects.filter(Q(gender = gender) | Q(gender = 'all'),min_money__lte = salary, max_money__gte = salary)
        

        for condition in conditions:
            if '%' in condition.amount:
                tmp = int(condition.amount[0:len(condition.amount)-1])
                tmp =((salary * tmp) / 100)
            else:
                tmp = int(condition.amount)
            tmp = max(tmp, condition.min_amount)
            if condition.global_component.component_type == 'compensation':
                final_pay += tmp
                payslip['description']['compensations'].append({
                    'name': condition.global_component.name,
                    'amount': tmp,
                })
            else:
                final_pay -= tmp
                payslip['description']['deductions'].append({
                    'name': condition.global_component.name,
                    'amount': tmp,
                })
        
        payslip['final_amount'] = final_pay

        if 'isEid' in data and data['isEid'] and employee.relegion == 'islam':
            payslip['description']['compensations'].append({'name': 'Eid Festival', 'amount': salary})
            payslip['final_amount'] += salary
        
        if 'isPuja' in data and data['isPuja'] and employee.relegion == 'hindu':
            payslip['description']['compensations'].append({'name': 'Puja Festival', 'amount': salary})
            payslip['final_amount'] += salary
        
        if 'isChristmas' in data and data['isChristmas'] and employee.relegion == 'christian':
            payslip['description']['compensations'].append({'name': 'Christmas Festival', 'amount': salary})
            payslip['final_amount'] += salary
        
        if 'isNewYear' in data and data['isNewYear']:
            payslip['description']['compensations'].append({'name': 'New Year Festival', 'amount': ((salary * 20) / 100)})
            payslip['final_amount'] += ((salary * 20) / 100)
        

        if fromDate.month == 6:
            taxFromDate = datetime.strptime(f'{fromDate.year - 1}-{fromDate.month + 1}-01', '%Y-%m-%d').date()
            taxToDate = datetime.strptime(f'{toDate.year}-{toDate.month}-{toDate.day}', '%Y-%m-%d').date()
            self.calculate_tax(employee, payslip, taxFromDate, taxToDate)
        
        return payslip
    

    def get(self, request):
        if request.user.department == None:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'Unauthorized'})
        
        payslips = request.user.department.dptPayslips.all()
        serializer = PayslipSerializer(payslips, many=True)

        return Response(serializer.data)


    def post(self, request):

        if request.user.department == None:
            return Response(status=status.HTTP_403_FORBIDDEN, data={'message': 'Unauthorized'})

        employees = request.user.department.employees.all()
        
        for employee in employees:
            payslip = self.calculate_payroll(employee, request.data)
            serializer = PayslipSerializer(data = payslip)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(status=status.HTTP_400_BAD_REQUEST, data={'message': 'server error'})

        
        return Response({'message': 'Calculated'})