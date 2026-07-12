"""
Role-based access control for MatriNest.

There are three roles:
  - admin   : request.user.is_staff or is_superuser. Granted only via
              `createsuperuser` or by another admin in the Django admin
              panel — never through the signup form. Admins can do
              everything: every view in this app, plus the full Django
              admin site at /admin/.
  - doctor  : request.user.user_type == 'doctor'. Can view the
              appointment queue and browse medicines, but cannot add,
              edit or delete medicines, and cannot see other users'
              health records.
  - patient : request.user.user_type == 'patient'. Can book and view
              their OWN appointments, log and view their OWN health
              records, and browse medicines — but cannot add, edit or
              delete medicines.

Usage:
    @role_required('patient', 'doctor')
    def some_view(request): ...

    @role_required('admin')          # admin-only view
    def upload_medicine(request): ...
"""
from functools import wraps
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect


def role_required(*roles):
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def _wrapped(request, *args, **kwargs):
            user = request.user
            if user.is_staff or user.is_superuser:
                return view_func(request, *args, **kwargs)
            if 'admin' in roles and not (user.is_staff or user.is_superuser):
                messages.error(request, "That action is reserved for administrators.")
                return redirect('home')
            if getattr(user, 'user_type', None) in roles:
                return view_func(request, *args, **kwargs)
            messages.error(request, "You don't have permission to do that.")
            return redirect('home')
        return _wrapped
    return decorator
