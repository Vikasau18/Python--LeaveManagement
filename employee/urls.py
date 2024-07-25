from django.urls import path
from . import views

urlpatterns = [
    path('leaverequest/', views.leave_request, name='leaverequest'),
    path('leavetype/', views.getLeaveType, name='leavetype'),
    path('getemployeeleaves/', views.getEmployeeLeaves, name='getemployeeleaves'),
    path('getEmployeeLeavesBal', views.getEmployeeLeavesBal, name='getEmployeeLeavesBal'),


]