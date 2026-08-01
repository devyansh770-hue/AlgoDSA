import json
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Submission
from apps.problems.models import Problem
from .services.judge0 import Judge0Service


@login_required
@require_POST
def submit_code(request):
    """Submit code for execution against test cases."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    code = data.get('code', '')
    language = data.get('language', 'python')

    if not problem_id or not code.strip():
        return JsonResponse({'error': 'Problem ID and code are required'}, status=400)

    problem = get_object_or_404(Problem, id=problem_id)
    test_cases = list(problem.test_cases.all())

    if not test_cases:
        return JsonResponse({'error': 'No test cases available for this problem'}, status=400)

    # Create submission record
    submission = Submission.objects.create(
        user=request.user,
        problem=problem,
        code=code,
        language=language,
        status='running',
        test_cases_total=len(test_cases),
    )

    # Execute via Judge0
    judge0 = Judge0Service()
    result = judge0.execute(code, language, test_cases)

    # Update submission
    submission.status = result['status']
    submission.runtime_ms = result['runtime_ms']
    submission.memory_kb = result['memory_kb']
    submission.test_cases_passed = result['test_cases_passed']
    submission.stdout = result.get('stdout', '')
    submission.stderr = result.get('stderr', '')
    submission.save()

    # Update user stats if accepted
    if result['status'] == 'accepted':
        user = request.user
        # Check if this is the first time solving this problem
        first_solve = not Submission.objects.filter(
            user=user,
            problem=problem,
            status='accepted'
        ).exclude(id=submission.id).exists()

        if first_solve:
            user.solved_count += 1
            user.save(update_fields=['solved_count'])

        # Update streak
        user.update_streak()

        # Update pattern mastery
        from apps.progress.services.spaced_repetition import update_mastery
        update_mastery(user, problem, correct=True)
    else:
        # Update mastery & create mistake log for incorrect submission
        from apps.progress.services.spaced_repetition import update_mastery
        from .models import MistakeRecord
        update_mastery(request.user, problem, correct=False)

        cat = 'tle' if result['status'] == 'time_limit' else ('pointer_bounds' if 'index out of range' in submission.stderr.lower() else 'general_logic')
        MistakeRecord.objects.create(
            user=request.user,
            submission=submission,
            problem=problem,
            error_category=cat,
            ai_remediation=f"Review test case failure on {problem.title}. Focus on pointer bounds and edge cases."
        )

    # Build response
    response_data = {
        'submission_id': submission.id,
        'status': result['status'],
        'status_display': submission.get_status_display(),
        'status_color': submission.status_color,
        'status_icon': submission.status_icon,
        'runtime_ms': result['runtime_ms'],
        'memory_kb': result['memory_kb'],
        'test_cases_passed': result['test_cases_passed'],
        'test_cases_total': result['test_cases_total'],
        'results': [r for r in result['results'] if r.get('is_sample', False)],  # Only show sample results
        'stdout': result.get('stdout', ''),
        'stderr': result.get('stderr', ''),
    }

    return JsonResponse(response_data)


@login_required
def submission_history(request):
    """View all submissions for the current user with rich analytics & filters."""
    all_user_subs = Submission.objects.filter(user=request.user).select_related('problem', 'problem__topic').order_by('-created_at')

    # Aggregate Statistics
    total_submissions_count = all_user_subs.count()
    accepted_count = all_user_subs.filter(status='accepted').count()
    wrong_answer_count = all_user_subs.filter(status='wrong_answer').count()
    runtime_error_count = all_user_subs.filter(status='runtime_error').count()
    time_limit_count = all_user_subs.filter(status__in=['time_limit', 'memory_limit']).count()
    compilation_error_count = all_user_subs.filter(status='compilation_error').count()

    acceptance_rate = round((accepted_count / total_submissions_count * 100), 1) if total_submissions_count > 0 else 0.0

    # Optional server-side filters
    submissions = all_user_subs
    status_filter = request.GET.get('status', '')
    if status_filter:
        if status_filter == 'accepted':
            submissions = submissions.filter(status='accepted')
        elif status_filter == 'wrong_answer':
            submissions = submissions.filter(status='wrong_answer')
        elif status_filter == 'runtime_error':
            submissions = submissions.filter(status='runtime_error')
        elif status_filter == 'time_limit':
            submissions = submissions.filter(status__in=['time_limit', 'memory_limit'])
        elif status_filter == 'compilation_error':
            submissions = submissions.filter(status='compilation_error')

    language_filter = request.GET.get('language', '')
    if language_filter:
        submissions = submissions.filter(language=language_filter)

    context = {
        'submissions': submissions[:100],
        'total_submissions_count': total_submissions_count,
        'accepted_count': accepted_count,
        'wrong_answer_count': wrong_answer_count,
        'runtime_error_count': runtime_error_count,
        'time_limit_count': time_limit_count,
        'compilation_error_count': compilation_error_count,
        'acceptance_rate': acceptance_rate,
        'status_filter': status_filter,
        'language_filter': language_filter,
    }
    return render(request, 'submissions/history.html', context)


@login_required
def submission_detail(request, submission_id):
    """View a single submission."""
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)
    
    all_subs = list(Submission.objects.filter(
        user=request.user,
        problem=submission.problem
    ).order_by('-created_at').values_list('id', flat=True))

    curr_index = all_subs.index(submission.id) if submission.id in all_subs else -1
    prev_id = all_subs[curr_index + 1] if curr_index != -1 and curr_index + 1 < len(all_subs) else None
    next_id = all_subs[curr_index - 1] if curr_index > 0 else None

    return render(request, 'submissions/detail.html', {
        'submission': submission,
        'prev_id': prev_id,
        'next_id': next_id,
        'submission_number': len(all_subs) - curr_index if curr_index != -1 else 1,
        'total_submissions': len(all_subs),
    })


@login_required
def get_problem_submissions_api(request, problem_id):
    """JSON endpoint to list all submissions for a problem by current user."""
    problem = get_object_or_404(Problem, id=problem_id)
    submissions = Submission.objects.filter(
        user=request.user,
        problem=problem
    ).order_by('-created_at')

    from django.utils.timesince import timesince

    data = []
    for sub in submissions:
        data.append({
            'id': sub.id,
            'status': sub.status,
            'status_display': sub.get_status_display(),
            'status_color': sub.status_color,
            'status_icon': sub.status_icon,
            'language': sub.language,
            'language_display': sub.get_language_display(),
            'runtime_ms': sub.runtime_ms,
            'memory_kb': sub.memory_kb,
            'test_cases_passed': sub.test_cases_passed,
            'test_cases_total': sub.test_cases_total,
            'created_at_relative': f"{timesince(sub.created_at)} ago",
            'created_at_formatted': sub.created_at.strftime('%b %d, %Y %H:%M:%S'),
        })

    return JsonResponse({'submissions': data})


@login_required
def get_submission_detail_api(request, submission_id):
    """JSON endpoint for detailed submission view with prev/next navigation."""
    submission = get_object_or_404(Submission, id=submission_id, user=request.user)

    all_subs = list(Submission.objects.filter(
        user=request.user,
        problem=submission.problem
    ).order_by('-created_at').values_list('id', flat=True))

    curr_index = all_subs.index(submission.id) if submission.id in all_subs else -1
    prev_id = all_subs[curr_index + 1] if curr_index != -1 and curr_index + 1 < len(all_subs) else None
    next_id = all_subs[curr_index - 1] if curr_index > 0 else None
    total_count = len(all_subs)
    submission_index = total_count - curr_index if curr_index != -1 else 1

    from django.utils.timesince import timesince

    data = {
        'id': submission.id,
        'problem_id': submission.problem.id,
        'problem_title': submission.problem.title,
        'problem_slug': submission.problem.slug,
        'topic_slug': submission.problem.topic.slug,
        'difficulty': submission.problem.difficulty,
        'difficulty_display': submission.problem.get_difficulty_display(),
        'code': submission.code,
        'language': submission.language,
        'language_display': submission.get_language_display(),
        'status': submission.status,
        'status_display': submission.get_status_display(),
        'status_color': submission.status_color,
        'status_icon': submission.status_icon,
        'runtime_ms': submission.runtime_ms,
        'memory_kb': submission.memory_kb,
        'test_cases_passed': submission.test_cases_passed,
        'test_cases_total': submission.test_cases_total,
        'stdout': submission.stdout,
        'stderr': submission.stderr,
        'failure_reason': submission.failure_reason,
        'ai_review': submission.ai_review,
        'created_at_relative': f"{timesince(submission.created_at)} ago",
        'created_at_formatted': submission.created_at.strftime('%b %d, %Y %H:%M:%S'),
        'prev_id': prev_id,
        'next_id': next_id,
        'submission_number': submission_index,
        'total_submissions': total_count,
    }
    return JsonResponse(data)


@login_required
def mistake_library(request):
    """Searchable mistake database recording failed runs & AI remediation (Feature: Mistake Library)."""
    from .models import MistakeRecord
    mistakes = MistakeRecord.objects.filter(user=request.user).select_related('problem', 'submission')
    
    # Filter by category if requested
    cat = request.GET.get('category')
    if cat:
        mistakes = mistakes.filter(error_category=cat)

    context = {
        'mistakes': mistakes,
        'selected_category': cat or '',
    }
    return render(request, 'submissions/mistakes.html', context)
