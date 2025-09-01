from django.http import HttpRequest
from django.shortcuts import redirect


def redirect_authenticated_users(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
    return wrapper