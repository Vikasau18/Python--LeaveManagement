from django.shortcuts import get_object_or_404, render
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.db.models import Sum
from employee.models import Employee, LeaveCredits, LeaveRequest, LeaveType
from employee.forms import *
from employee.serializers import *
@csrf_exempt
@api_view(['POST', 'GET'])
def getEmployeeLeaves(request):
    leave_requests = LeaveRequest.objects.select_related('employee','leavetype').values(
        'uid',
        'employee_id', 
        'from_date', 
        'to_date', 
        'reason', 
        'leavetype_id', 
        'leavetype__leavetype', 
        'reason',
        'status',
        'numberofdays'
    )    
    leave_requests_list = list(leave_requests)
    return JsonResponse({
        'leave_requests': leave_requests_list,
        'status': 'success',
        'msg': 'Leave Requests retrieved successfully'
    }, status=200)

# @csrf_exempt
# @api_view(['POST'])
# def changeleavestatus(request, id):
#     try:
#         obj = LeaveRequest.objects.get(uid=id)
#         form = LeaveRequestForm(instance=obj)
#         print(obj)
#     except LeaveRequest.DoesNotExist:
#         return Response({
#             'status': 'error',
#             'msg': 'Leave Request not found'
#         }, status=status.HTTP_404_NOT_FOUND)    
#     if request.method == 'POST':
#         form = LeaveRequestForm(request.POST, instance=obj)
#         if form.is_valid():
#             form.save()
#             return Response({
#             'status': 'success',
#             'msg': 'Leave Request updated successfully'
#         }, status=status.HTTP_200_OK)
#         else:
#             return Response({
#             'status': 'failure',
#             'msg': form.errors
#         }, status=status.HTTP_200_OK)
@csrf_exempt
@api_view(['POST'])
def changeleavestatus(request, id, *args, **kwargs):
    req = get_object_or_404(LeaveRequest, uid=id)
    if not req:
        return Response(
            {"res": "Object with req id does not exist"}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    data = {
        'status': request.data.get('status'), 
    }
    serializer = LeaveRequestSerializer(instance=req, data=data, partial=True)
    if serializer.is_valid():
        serializer.save()
        leave_data=LeaveRequest.objects.filter(uid=id).values('employee_id', 'leavetype_id', 'numberofdays').first()
        updateremainingleaves(
                leave_data['numberofdays'],
                leave_data['leavetype_id'],
                leave_data['employee_id']
            )       
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



def updateremainingleaves(number_of_days, leavetype_id, employee_id):
    print('--------------------------------------print-------------------------------')

    # Retrieve LeaveCredits object if it exists
    req = LeaveCredits.objects.filter(leavetype_id=leavetype_id, employee_id=employee_id).first()

    # If the record was found, update the remaining days
    if not req:
        leave_type = get_object_or_404(LeaveType, uid=leavetype_id)
        remaining_days = leave_type.defaultdays - int(number_of_days)
        data = {
            "remainingleavedays": remaining_days,
            "leavetype": leavetype_id,
            "employee": employee_id
        }

        serializer = LeaveCreditsSerializer(instance=req, data=data, partial=True)
    else:
        req.remainingleavedays=req.remainingleavedays-int(number_of_days)
        
        # If a new record was created, use the initial data
        data = {
            "remainingleavedays": req.remainingleavedays,
            "leavetype": leavetype_id,
            "employee": employee_id
        }
        serializer = LeaveCreditsSerializer(instance=req, data=data, partial=True)

    # Update serializer with the new data and save
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view([ 'GET'])
def getLeaveBalance(request):
   
    # Calculate total days from LeaveType (assuming there's only one instance)
    total_days = LeaveType.objects.aggregate(total=Sum('defaultdays'))['total']
    
    # Prepare a list to hold the final data
    leave_balance_list = []
    
    # Iterate through each employee to calculate and append data
    employees = Employee.objects.all()
    for emp in employees:
        employee_name = emp.name
        
        # Attempt to retrieve LeaveCredits for the employee
        taken_days = LeaveRequest.objects.filter(employee_id=emp.uid, status='Approved').aggregate(total=Sum('numberofdays'))['total']
        
        if taken_days is not None:
            total_taken_days = taken_days
            total_remains = total_days-taken_days
        else:
            total_taken_days = None
            total_remains = None
        
        # Prepare the dictionary for the employee's leave balance
        leave_balance = {
            'employee_name': employee_name,
            'total_taken_days': total_taken_days,
            'total_remains': total_remains,
            'total_days': total_days,
        }
        
        leave_balance_list.append(leave_balance)

    return JsonResponse({
        'leave_balance': leave_balance_list,
        'status': 'success',
        'msg': 'Leave balance retrieved successfully'
    }, status=200)