"""
Accounts App Views
Handles user authentication and profile management:
- Registration with email verification
- Login and logout
- Email verification
- Profile viewing and editing
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from .models import UserProfile
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm


#------------------
#    REGISTRATION
#------------------

@require_http_methods(["GET", "POST"])
def register(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                # Create profile and token
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.generate_verification_token()
                
                try:
                    # Attempt to send, but we catch the failure immediately
                    profile.send_verification_email() 
                    messages.success(request, 'Account created! Please check your email to verify.')
                    return redirect('accounts:email_verification') # Redirect to the info page
                except Exception as e:
                    # EMAIL FAILED: Don't hang the UI. 
                    # Auto-verify them so they aren't locked out of their new account.
                    profile.email_verified = True
                    profile.save()
                    login(request, user) 
                    messages.warning(request, 'Welcome! We couldn’t send a verification email right now, but your account is ready.')
                    return redirect('tasks:dashboard')

            except IntegrityError:
                form.add_error('email', 'This email address is already registered.')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'auth/register.html', {'form': form})


#------------------
#  EMAIL VERIFICATION
#------------------
@require_http_methods(["GET"])
def verify_email(request, token):
    try:
        profile = get_object_or_404(UserProfile, email_verification_token=token)
        profile.email_verified = True
        profile.email_verification_token = None
        profile.save()
        messages.success(request, 'Email verified successfully! You can now login.')
        return redirect('accounts:login')
    except Exception:
        messages.error(request, 'Invalid verification token.')
        return redirect('accounts:email_verification')


@require_http_methods(["GET"])
def email_verification(request):
    return render(request, 'auth/verify_email.html')


#------------------
#    LOGIN / LOGOUT
#------------------

@require_http_methods(["GET", "POST"])
def login_view(request):
    if request.user.is_authenticated:
        return redirect('tasks:dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=username_or_email, password=password)

            if not user:
                try:
                    user_obj = User.objects.get(email=username_or_email)
                    user = authenticate(request, username=user_obj.username, password=password)
                except User.DoesNotExist:
                    user = None

            if user:
                profile, _ = UserProfile.objects.get_or_create(user=user)
                
                if not profile.email_verified:
                    messages.warning(request, "Welcome! Please remember to verify your email when you can.")
                else:
                    messages.success(request, f"Welcome back, {user.username}!")

                login(request, user)
                next_url = request.GET.get('next')
                return redirect(next_url or 'tasks:dashboard')
            else:
                messages.error(request, 'Invalid username/email or password.')
    else:
        form = UserLoginForm()

    return render(request, 'auth/login.html', {'form': form})


@require_http_methods(["GET"])
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('tasks:home')


#------------------
#    PROFILE EDIT
#------------------
@login_required(login_url='accounts:login')
@require_http_methods(["GET", "POST"])
def edit_profile(request):
    profile, created = UserProfile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            # Update User model fields
            user = request.user
            user.first_name = form.cleaned_data.get('first_name', '')
            user.last_name = form.cleaned_data.get('last_name', '')
            user.email = form.cleaned_data.get('email', user.email)
            user.save()
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:edit_profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = UserProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        })

    tasks_count = request.user.tasks.count()
    completed_count = request.user.tasks.filter(is_completed=True).count()

    context = {
        'form': form,
        'profile': profile,
        'tasks_count': tasks_count,
        'completed_count': completed_count,
    }

    return render(request, 'tasks/profile.html', context)


#------------------
#    DELETE ACCOUNT
#------------------
@login_required
def delete_account(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account has been permanently deleted. We're sorry to see you go!")
        return redirect('tasks:home')
    return redirect('accounts:edit_profile')