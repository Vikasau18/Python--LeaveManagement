from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Employee, Role, UserRole

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        try:
            existing_users_count = User.objects.count()
            if existing_users_count == 0:
                role_name = 'admin'
            else:
                role_name = 'employee'
            # Create the User instance
            user = User.objects.create_user(
                username=validated_data['username'],
                password=validated_data['password'],
                email=validated_data['email']
            )
          # Retrieve or create the Role instance
            role, _ = Role.objects.get_or_create(name=role_name)
            user_role = UserRole.objects.create(user=user, role=role)

            return user
        
        except Exception as e:
            print(f"Error creating user or employee: {e}")
            raise serializers.ValidationError("Failed to create user or employee")
