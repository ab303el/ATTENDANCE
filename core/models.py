from django.db import models
from django.contrib.auth.models import User  # Import Django's built-in User


class Employee(models.Model):

    # Real-World Principle: One-to-One Link
    # Every Employee profile is linked to exactly one User account for login.
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True , blank=True)
    name = models.CharField(max_length=100)
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    date = models.DateField(auto_now_add=True)
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.name} - {self.date}"

    class Meta:
        unique_together = ('employee', 'date')
