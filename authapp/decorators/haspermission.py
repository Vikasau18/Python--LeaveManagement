from functools import wraps
from django.http import HttpResponseForbidden, JsonResponse, HttpResponseBase
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from authapp.models import Role, UserRole

def has_permission(perm_name):
    """
    Decorator to require specific permissions for API views.
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({'error': 'Authentication Required'}, status=401)

            user_role = UserRole.objects.filter(user_id=request.user.id).first()
            role=Role.objects.filter(id=user_role.role_id).first()
            if role.name==perm_name:
                return view_func(request, *args, **kwargs)
            return JsonResponse({'error': 'Permission denied'}, status=403)
     
        return wrapper
    
    return decorator
