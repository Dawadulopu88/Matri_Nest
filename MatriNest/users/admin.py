from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Full admin control over every user — the admin role is granted by
    is_staff/is_superuser (set here or via `createsuperuser`), and is
    completely separate from the patient/doctor `user_type` field below.
    """
    list_display = ('username', 'email', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('MatriNest role', {'fields': ('user_type',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('MatriNest role', {'fields': ('user_type', 'email')}),
    )
