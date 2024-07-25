from django.urls import path
from . import views

urlpatterns = [
    path('getemployeeleaves/', views.getEmployeeLeaves, name='getemployeeleaves'),
    path('changeleavestatus/<uuid:id>', views.changeleavestatus, name='changeleavestatus'),
    path('updateremainingleaves', views.updateremainingleaves, name='updateremainingleaves'),
    path('getLeaveBalance',views.getLeaveBalance, name='getLeaveBalance')

]