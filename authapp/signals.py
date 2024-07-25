# authapp/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from employee.models import Employee  # Import the Employee model from the employee app

@receiver(post_save, sender=User)
def create_employee(sender, instance, created, **kwargs):
   
    if created:
        print(instance.id)
        Employee.objects.create(
            name=instance,
            email=instance.email,
            user_id=instance.id,
            address=''  # You can provide default values or handle this differently
        )
