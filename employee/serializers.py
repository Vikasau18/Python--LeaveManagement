from rest_framework import serializers
from .models import LeaveCredits, LeaveRequest

class LeaveRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveRequest
        fields = '__all__'

class LeaveCreditsSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveCredits
        fields = '__all__'
