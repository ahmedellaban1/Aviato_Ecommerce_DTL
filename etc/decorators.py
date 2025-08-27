from functools import wraps
from django.shortcuts import redirect

def client_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated:
            if getattr(request.user, "type", None) != "client":
                return redirect('/admin/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
