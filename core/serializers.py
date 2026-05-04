from rest_framework import serializers
from .models import Attendance , Employee

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['id' , 'name' , 'employee_id']

class AttendanceSerializer(serializers.ModelSerializer):
    # This automatically nests the employee details or just gives the ID
    class Meta:
        model = Attendance
        fields = ['id' , 'employee' , 'date' , 'clock_in' , 'clock_out']
