from functools import wraps
from django.http import HttpResponseForbidden
from django.http import JsonResponse
def login_required_api(view_func):
    """
    Decorator to require login for API views.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            # User is authenticated, allow access to the view
            return view_func(request, *args, **kwargs)
        else:
            # User is not authenticated, return a JSON response with error
            return JsonResponse({'error': 'Authentication Required'}, status=401)
    return wrapper