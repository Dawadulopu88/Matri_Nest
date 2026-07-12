from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import CustomUser
from myapp.forms import ProfileForm


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user_type = request.POST.get('user_type', 'patient')

        if not email or not username or not password:
            messages.error(request, "All fields are required.")
            return redirect('signup')
        if user_type not in ('patient', 'doctor'):
            user_type = 'patient'
        if CustomUser.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email already registered.")
            return redirect('signup')
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, "Username already taken.")
            return redirect('signup')

        # NOTE: account creation here only ever sets user_type to patient or
        # doctor. Admin (is_staff/is_superuser) is never granted through
        # signup — only via `createsuperuser` or by an existing admin.
        user = CustomUser.objects.create_user(
            email=email, username=username,
            password=password, user_type=user_type,
        )
        login(request, user, backend='users.backends.EmailBackend')
        messages.success(request, f"Welcome, {username}! Your account has been created.")
        return redirect('home')
    return render(request, 'Auth/signup.html')


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        messages.error(request, "Invalid email or password.")
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, "You have been logged out.")
    return redirect('welcome')


def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    profile = request.user.profile
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect('profile')
    return render(request, 'Auth/profile.html', {'user': request.user, 'form': form})
