from django.shortcuts import render

from employee.decorators.login import login_required_api
from authapp.decorators.haspermission import has_permission
from .forms import LeaveRequestForm
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import *
from .serializers import LeaveRequestSerializer
@csrf_exempt
@api_view(['POST'])
def leave_request(request):
    serializer = LeaveRequestSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({
            'status': 'success',
            'msg': 'Leave Request Sent'
        }, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST', 'GET'])
def getLeaveType(request):
    leave_types = LeaveType.objects.all().values()
    leave_types_list = list(leave_types)
    return JsonResponse({
        'type': leave_types_list,
        'status': 'success',
        'msg': 'Leave types retrieved successfully'
    }, status=200)

@csrf_exempt
@api_view(['POST', 'GET'])
def getEmployeeLeaves(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')  # Get user_id from query parameters
        print(user_id)
    if user_id:
        leave_requests = LeaveRequest.objects.filter(employee=user_id).values()
    else:
        leave_requests = LeaveRequest.objects.all().values()
    leave_requests_list = list(leave_requests)
    return JsonResponse({
        'leave_requests': leave_requests_list,
        'status': 'success',
        'msg': 'Leave Requests retrieved successfully'
    }, status=200)

@csrf_exempt
@api_view(['GET'])
def getEmployeeLeavesBal(request):
    if request.method == 'GET':
        user_id = request.GET.get('user_id')  # Get user_id from query parameters
  
    leave_credits = LeaveCredits.objects.filter(employee_id=user_id).select_related('LeaveCredits','leavetype').values(
            'leavetype__leavetype',
            'remainingleavedays',
            'leavetype__defaultdays'
        )
    leave_balance_list = []
    leave_requests_list = list(leave_credits)
    for leave in leave_credits:
          bal_percentage=leave['remainingleavedays']/leave['leavetype__defaultdays']*100
          leave_balance = {
            'remainingdays': leave['remainingleavedays'],
            'leavetype':leave['leavetype__leavetype'],
            'bal_percentage': bal_percentage,
            'defaultdays':leave['leavetype__defaultdays']

        }    
          leave_balance_list.append(leave_balance)

    return JsonResponse({
        'leave_balance': leave_balance_list,
        'status': 'success',
        'msg': 'Leave Balance retrieved successfully'
    }, status=200)