from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .forms import CustomUserCreationForm, UserProfileForm
from .models import User


def check_username_api(request):
    """AJAX endpoint to check username availability."""
    username = request.GET.get('username', '').strip()
    if not username:
        return JsonResponse({'valid': False, 'available': False, 'message': 'Username is required'})

    if len(username) < 3:
        return JsonResponse({'valid': False, 'available': False, 'message': 'Minimum 3 characters required'})

    exists = User.objects.filter(username__iexact=username).exists()
    if exists:
        return JsonResponse({'valid': True, 'available': False, 'message': 'Username already taken'})
    return JsonResponse({'valid': True, 'available': True, 'message': 'Username available'})


def check_email_api(request):
    """AJAX endpoint to check email format and availability."""
    email = request.GET.get('email', '').strip()
    if not email:
        return JsonResponse({'valid': True, 'available': True, 'message': 'Email is optional'})

    try:
        validate_email(email)
    except ValidationError:
        return JsonResponse({'valid': False, 'available': False, 'message': 'Invalid email format'})

    exists = User.objects.filter(email__iexact=email).exists()
    if exists:
        return JsonResponse({'valid': True, 'available': False, 'message': 'Email already registered'})
    return JsonResponse({'valid': True, 'available': True, 'message': 'Email format valid & available'})



def landing_page(request):
    """Landing page — redirect to dashboard if authenticated."""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'landing.html')


def register_view(request):
    """User registration."""
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome to AlgoDSA, {user.username}! 🚀')
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()

    return render(request, 'registration/register.html', {'form': form})


def logout_view(request):
    """Logout user."""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('landing')


@login_required
def profile_view(request):
    """User profile page."""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated! ✅')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    # Get user stats
    from apps.submissions.models import Submission
    from apps.progress.models import PatternMastery

    recent_submissions = Submission.objects.filter(
        user=request.user
    ).order_by('-created_at')[:10]

    masteries = PatternMastery.objects.filter(
        user=request.user
    ).order_by('-mastery_score')

    context = {
        'form': form,
        'recent_submissions': recent_submissions,
        'masteries': masteries,
    }
    return render(request, 'users/profile.html', context)
