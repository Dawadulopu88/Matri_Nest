from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Medicine, Appointment, HealthRecord
from .forms import MedicineForm, AppointmentForm, HealthRecordForm
from .decorators import role_required


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request, 'welcome.html')


@login_required
def home(request):
    return render(request, 'myapp/home.html')


def about(request):
    return render(request, 'myapp/about.html')


def help_view(request):
    return render(request, 'help.html')


# --- Medicine: browsing is open to every logged-in role; managing the
# catalogue (add/edit/delete) is admin-only. ---

def medicine_list(request):
    q = request.GET.get('q', '')
    medicines = Medicine.objects.filter(medicine_name__icontains=q) if q else Medicine.objects.all()
    return render(request, 'myapp/all_medicines.html', {'medicines': medicines, 'query': q})


def medicine_details(request, id):
    medicine = get_object_or_404(Medicine, pk=id)
    return render(request, 'myapp/details_medicine.html', {'medicine': medicine})


@role_required('admin')
def upload_medicine(request):
    form = MedicineForm()
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES)
        if form.is_valid():
            medicine = form.save(commit=False)
            medicine.created_by = request.user
            medicine.save()
            messages.success(request, 'Medicine added successfully!')
            return redirect('medicine_list')
    return render(request, 'myapp/medicine_form.html', {'form': form, 'action': 'Add'})


@role_required('admin')
def update_medicine(request, id):
    medicine = get_object_or_404(Medicine, pk=id)
    form = MedicineForm(instance=medicine)
    if request.method == 'POST':
        form = MedicineForm(request.POST, request.FILES, instance=medicine)
        if form.is_valid():
            form.save()
            messages.success(request, 'Medicine updated successfully!')
            return redirect('medicine_list')
    return render(request, 'myapp/medicine_form.html', {'form': form, 'action': 'Update'})


@role_required('admin')
def delete_medicine(request, id):
    medicine = get_object_or_404(Medicine, pk=id)
    if request.method == 'POST':
        medicine.delete()
        messages.success(request, 'Medicine deleted.')
        return redirect('medicine_list')
    return render(request, 'myapp/delete_medicine.html', {'medicine': medicine})


# --- Appointments: patients book and see only their own; doctors and
# admins see the full queue read-only. ---

@role_required('patient', 'doctor')
def appoint_view(request):
    user = request.user

    if user.is_patient:
        form = AppointmentForm()
        if request.method == 'POST':
            form = AppointmentForm(request.POST)
            if form.is_valid():
                appt = form.save(commit=False)
                appt.user = user
                appt.save()
                messages.success(request, 'Appointment booked successfully!')
                return redirect('appoint')
        appointments = Appointment.objects.filter(user=user)
        return render(request, 'myapp/appoint.html', {
            'form': form, 'appointments': appointments, 'can_book': True,
        })

    # Doctors (and staff) see the full queue, read-only — no booking form.
    appointments = Appointment.objects.all()
    return render(request, 'myapp/appoint.html', {
        'form': None, 'appointments': appointments, 'can_book': False,
    })


# --- Health tracking: strictly private to the patient who owns the data. ---

@role_required('patient')
def health_view(request):
    form = HealthRecordForm()
    records = HealthRecord.objects.filter(user=request.user)[:10]
    if request.method == 'POST':
        form = HealthRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.user = request.user
            record.save()
            messages.success(request, 'Health data saved!')
            return redirect('health')
    return render(request, 'myapp/healthtrack.html', {'form': form, 'records': records})


# --- Simple service pages: open to any logged-in patient or doctor. ---

@role_required('patient', 'doctor')
def emergency_view(request):
    return render(request, 'myapp/emergency.html')


@role_required('patient', 'doctor')
def nurse_view(request):
    return render(request, 'myapp/hirenurse.html')


@role_required('patient', 'doctor')
def ambulance_view(request):
    return render(request, 'myapp/bookambulance.html')


@role_required('patient', 'doctor')
def mental_view(request):
    return render(request, 'myapp/mentalhealth.html')
