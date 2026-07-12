from django import forms
from .models import Medicine, Appointment, HealthRecord, UserProfile


class MedicineForm(forms.ModelForm):
    class Meta:
        model = Medicine
        fields = ['medicine_name', 'description', 'price', 'image']
        widgets = {
            'medicine_name': forms.TextInput(attrs={'placeholder': 'Medicine name'}),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Description'}),
            'price': forms.NumberInput(attrs={'placeholder': '0.00', 'step': '0.01'}),
        }


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = ['user', 'created_at']
        widgets = {
            'full_name': forms.TextInput(attrs={'placeholder': 'Your full name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'your@email.com'}),
            'doctor_name': forms.TextInput(attrs={'placeholder': 'Doctor name'}),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'reason': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe your reason...'}),
        }


class HealthRecordForm(forms.ModelForm):
    class Meta:
        model = HealthRecord
        exclude = ['user', 'created_at']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'weight': forms.NumberInput(attrs={'placeholder': 'e.g. 65.5', 'step': '0.1'}),
            'blood_pressure': forms.TextInput(attrs={'placeholder': 'e.g. 120/80'}),
            'glucose': forms.NumberInput(attrs={'placeholder': 'mg/dL', 'step': '0.1'}),
            'symptoms': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Any symptoms...'}),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'phone', 'address', 'profile_picture']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'placeholder': 'A little about you'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone number'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Address'}),
        }
