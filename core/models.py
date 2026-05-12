from django.db import models
from django.contrib.auth.models import User , Group # Import Django's built-in User 
from django.db.models.signals import post_save # user profile
from django.dispatch import receiver

@receiver(post_save, sender=User)
def manage_employee_profile(sender, instance, created, **kwargs):
    # Only act if the user is NOT a staff member
    if not instance.is_staff:
        Employee.objects.get_or_create(
            user=instance,
            defaults={
                'first_name': instance.first_name or instance.username,
                'last_name': instance.last_name or "",
                'email': instance.email,
                'employee_id': f"EMP-{instance.id}"
            }
        )
    else:
        # Optional: If an admin (staff) was previously an employee, 
        # you might want to remove them from the Employee table.
        # Remove the '#' below if you want to auto-delete admin records:
        # Employee.objects.filter(user=instance).delete()
        pass

@receiver(post_save, sender=User)
def save_employee_profile(sender, instance, **kwargs):
    # This ensures that if the User is updated, the Employee stays linked
    if hasattr(instance, 'employee'):
        # Update employee fields if user fields changed
        instance.employee.email = instance.email
        instance.employee.name = f"{instance.first_name} {instance.last_name}".strip() or instance.username
        instance.employee.save()

class Employee(models.Model):

    # Real-World Principle: One-to-One Link
    # Every Employee profile is linked to exactly one User account for login.
    user = models.OneToOneField(User , on_delete=models.CASCADE , null=True , blank=True)
    first_name = models.CharField(max_length=100 , null=True , blank=True)
    last_name = models.CharField(max_length=100 , null=True , blank=True)
    email = models.EmailField(null=True , blank=True)
    employee_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.first_name}  {self.last_name}"

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    
    date = models.DateField(auto_now_add=True)
    clock_in = models.DateTimeField(auto_now_add=True)
    clock_out = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.employee.first_name} - {self.date}"

    class Meta:
        unique_together = ('employee', 'date')
        ordering  = ['-date' , '-clock_in']
