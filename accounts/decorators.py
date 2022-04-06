from django.http import HttpResponse
from django.contrib import messages
from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowedUsers(allowed_roles = []):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_roles:
                return view_func(request, *args, **kwargs)
            else:
               return  HttpResponse(' {} You are not authorized to view this page'.format(request.user))               #  return redirect('accounts:login')
        return wrapper_func
    return decorator


def adminonly(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        if group == 'customer':
            return redirect('accounts:userpage')
        else:
            return view_func(request, *args, **kwargs)
    return wrapper_func

