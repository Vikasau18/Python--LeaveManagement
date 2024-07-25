from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import *

class Base(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Employee(Base):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    


class Role(models.Model):
    name = models.CharField(max_length=50)
    permissions = models.ManyToManyField(Permission)
    
class UserRole(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)