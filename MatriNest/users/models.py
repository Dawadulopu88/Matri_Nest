from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    """
    Custom user model with a role field.
    Roles:
      - patient: books appointments, tracks own health, browses medicines.
      - doctor:  views the appointment queue, browses medicines.
      - Full admin rights (everything, including Django admin) are granted
        through Django's built-in is_staff / is_superuser flags, set via
        `createsuperuser` or in the admin panel — NOT through user_type.
    """
    USER_TYPE_CHOICES = (
        ('patient', 'Patient'),
        ('doctor', 'Doctor'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='patient')
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    @property
    def is_patient(self):
        return self.user_type == 'patient'

    @property
    def is_doctor(self):
        return self.user_type == 'doctor'

    @property
    def is_admin_role(self):
        return self.is_staff or self.is_superuser
