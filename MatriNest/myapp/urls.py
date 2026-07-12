from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_view, name='welcome'),
    path('home/', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('help/', views.help_view, name='help'),

    # Medicine
    path('medicines/', views.medicine_list, name='medicine_list'),
    path('medicines/detail/<int:id>/', views.medicine_details, name='medicine_details'),
    path('medicines/upload/', views.upload_medicine, name='upload_medicine'),
    path('medicines/update/<int:id>/', views.update_medicine, name='update_medicine'),
    path('medicines/delete/<int:id>/', views.delete_medicine, name='delete'),

    # Services
    path('appoint/', views.appoint_view, name='appoint'),
    path('health/', views.health_view, name='health'),
    path('ambulance/', views.ambulance_view, name='ambulance'),
    path('emergency/', views.emergency_view, name='emergency'),
    path('mental/', views.mental_view, name='mental'),
    path('nurse/', views.nurse_view, name='nurse'),
]
