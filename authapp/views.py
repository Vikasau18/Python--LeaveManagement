# myapp/views.py

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from employee.models import Employee

from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
@api_view(['POST', 'GET'])
def signup(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    elif request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

@csrf_exempt
@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        if username and password:
            user = User.objects.filter(username=username).first()

            if user and user.check_password(password):
                refresh = RefreshToken.for_user(user)
                userid=Employee.objects.filter(user_id=user.id).values().first()
                return Response({
                    'tokens': {
                        'refresh': str(refresh),
                        'access': str(refresh.access_token),
                        'userid': str(userid['uid']),
                    }
                })
            else:
                return Response({'error': 'Incorrect credentials. Please try again.'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Must include username and password in request.'}, status=status.HTTP_400_BAD_REQUEST)