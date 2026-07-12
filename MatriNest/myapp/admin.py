from django.contrib import admin
from .models import Medicine, Appointment, HealthRecord, UserProfile


@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    list_display = ('medicine_name', 'price', 'created_by')
    search_fields = ('medicine_name',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'doctor_name', 'specialization', 'date', 'time', 'user')
    list_filter = ('specialization', 'date')
    search_fields = ('full_name', 'doctor_name', 'email')


@admin.register(HealthRecord)
class HealthRecordAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight', 'blood_pressure', 'glucose')
    list_filter = ('date',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone')
