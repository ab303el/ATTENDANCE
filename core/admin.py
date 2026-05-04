from django.contrib import admin
from .models import Attendance , Employee

# Register your models here.
# admin.site.register(Attendance)
# admin.site.register(Employee)

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('employee' ,'clock_in' , 'clock_out')
    fields = ('employee' , 'clock_out')
    readonly_fields = ('clock_in',)
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('name' , 'employee_id')
