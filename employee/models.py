from django.db import models
from django.contrib.auth.models import User
import uuid

class Base(models.Model):
    uid = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    date_created = models.DateTimeField(auto_now_add=True, blank=True)
    date_updated = models.DateTimeField(auto_now=True, blank=True)

    class Meta:
        abstract = True


class Employee(Base):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employee',  blank=True)
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class LeaveType(Base):
    leavetype = models.CharField(max_length=255)
    defaultdays = models.IntegerField()

    def __str__(self):
        return self.leavetype

class LeaveRequest(Base):
    reason = models.CharField(max_length=255)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    from_date = models.DateField()
    to_date = models.DateField()
    numberofdays = models.IntegerField()
    status = models.CharField(max_length=255, null=True)
    leavetype = models.ForeignKey(LeaveType, on_delete=models.CASCADE,  related_name='leave_requests')


    def __str__(self):
        return f"{self.employee.name} - {self.reason}"

class LeaveCredits(Base):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_credits')
    leavetype = models.ForeignKey(LeaveType, on_delete=models.CASCADE)
    remainingleavedays = models.IntegerField()

    def __str__(self):
        return f"{self.employee.name} - {self.leavetype.leavetype}"
