from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps
from django.http import HttpResponseForbidden

def admin_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'administrador':
            return function(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requieren permisos de administrador.')
        return redirect('index')
    return wrap

def difusor_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'difusor':
            return function(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requieren permisos de difusor.')
        return redirect('index')
    return wrap

def estudiante_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario == 'estudiante':
            return function(request, *args, **kwargs)
        messages.error(request, 'Acceso denegado. Se requieren permisos de estudiante.')
        return redirect('index')
    return wrap

def no_difusor_required(function):
    @wraps(function)
    def wrap(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.tipo_usuario != 'difusor':
            return function(request, *args, **kwargs)
        messages.error(request, 'Los difusores no pueden acceder a esta sección.')
        return redirect('index')
    return wrap