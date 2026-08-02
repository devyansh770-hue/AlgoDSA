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
            messages.success(request, 'Profile updated successfully! 🚀')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)

    from django.utils import timezone
    from django.db.models import Avg
    from apps.submissions.models import Submission
    from apps.progress.models import PatternMastery

    user = request.user
    recent_submissions = Submission.objects.filter(
        user=user
    ).select_related('problem').order_by('-created_at')[:10]

    masteries = PatternMastery.objects.filter(
        user=user
    ).order_by('-mastery_score')

    total_submissions = Submission.objects.filter(user=user).count()
    accepted_submissions = Submission.objects.filter(user=user, status='accepted').count()
    acceptance_rate = round((accepted_submissions / total_submissions * 100), 1) if total_submissions > 0 else 0.0

    avg_mastery_dict = masteries.aggregate(Avg('mastery_score'))
    avg_mastery = round(avg_mastery_dict['mastery_score__avg'] or 0.0, 1)

    today = timezone.now().date()
    due_reviews = [m for m in masteries if m.next_review and m.next_review <= today]

    # Calculate FAANG Readiness Score
    solved_metric = min(100, (user.total_platform_solved / 50.0) * 40)
    mastery_metric = (avg_mastery / 100.0) * 40
    streak_metric = min(20, user.streak * 2)
    readiness_score = int(min(99, solved_metric + mastery_metric + streak_metric))
    if readiness_score == 0 and user.total_platform_solved > 0:
        readiness_score = 45

    # 28-day practice activity heatmap data
    import datetime
    heatmap_days = []
    for i in range(27, -1, -1):
        day_date = today - datetime.timedelta(days=i)
        sub_count = Submission.objects.filter(
            user=user,
            created_at__date=day_date
        ).count()
        heatmap_days.append({
            'date': day_date.strftime('%b %d'),
            'count': sub_count,
            'level': 0 if sub_count == 0 else (1 if sub_count == 1 else (2 if sub_count <= 3 else 3))
        })

    context = {
        'form': form,
        'recent_submissions': recent_submissions,
        'masteries': masteries,
        'total_submissions': total_submissions,
        'accepted_submissions': accepted_submissions,
        'acceptance_rate': acceptance_rate,
        'avg_mastery': avg_mastery,
        'due_reviews': due_reviews,
        'due_reviews_count': len(due_reviews),
        'readiness_score': readiness_score,
        'heatmap_days': heatmap_days,
    }
    return render(request, 'users/profile.html', context)

