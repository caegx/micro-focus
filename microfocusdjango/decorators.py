from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.role == 'school':
            return redirect('school_dashboard')
        
        elif request.user.is_authenticated and request.user.role == 'admin':
            return redirect('admin_dashboard')
        
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func