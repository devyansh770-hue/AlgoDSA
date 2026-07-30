from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from .models import PatternMastery, TopicProgress
from .services.spaced_repetition import get_recommended_problems
from .services.leetcode import LeetCodeSyncService
from .services.gfg import GFGSyncService
from .services.platform_analytics import MultiPlatformAnalyticsService
from apps.submissions.models import Submission
from apps.problems.models import Problem


@login_required
def dashboard(request):
    """Main dashboard showing user's DSA progress, LeetCode & GeeksforGeeks multi-platform stats."""
    user = request.user

    # Multi-platform Analytics Engine
    analytics_service = MultiPlatformAnalyticsService(user)
    analytics = analytics_service.get_comprehensive_analytics()

    # Pattern mastery data
    masteries = PatternMastery.objects.filter(user=user).order_by('-mastery_score')

    # Topic progress data
    topic_progresses = TopicProgress.objects.filter(user=user).select_related('topic')

    # Recommended problems
    recommended = get_recommended_problems(user, limit=5)

    # Weakest pattern
    weakest = masteries.last() if masteries.exists() else None

    # Recent submissions — group consecutive same-problem entries
    raw_submissions = list(
        Submission.objects.filter(user=user)
        .select_related('problem')
        .order_by('-created_at')[:50]
    )
    recent_activity = _group_recent_activity(raw_submissions, max_entries=10)

    # Stats
    total_problems = Problem.objects.filter(is_active=True).count()
    accepted_count = Submission.objects.filter(
        user=user, status='accepted'
    ).values('problem').distinct().count()

    # LeetCode Synced problems count (matched in AlgoDSA curated set)
    leetcode_synced_count = Submission.objects.filter(
        user=user, status='accepted', is_leetcode_synced=True
    ).values('problem').distinct().count()

    # Remaining problems count in AlgoDSA database
    remaining_count = max(0, total_problems - accepted_count)

    # Completion percentage for AlgoDSA curated problem set
    completion_pct = int((accepted_count / total_problems * 100)) if total_problems > 0 else 0

    # Activity data (last 30 days)
    from django.utils import timezone
    from datetime import timedelta
    from django.db.models import Count
    from django.db.models.functions import TruncDate

    thirty_days_ago = timezone.now() - timedelta(days=30)
    daily_activity = (
        Submission.objects.filter(user=user, created_at__gte=thirty_days_ago)
        .annotate(date=TruncDate('created_at'))
        .values('date')
        .annotate(count=Count('id'))
        .order_by('date')
    )

    # Difficulty distribution — merge local DB + LC/GFG API data
    local_easy = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='easy'
    ).values('problem').distinct().count()
    local_medium = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='medium'
    ).values('problem').distinct().count()
    local_hard = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='hard'
    ).values('problem').distinct().count()

    # Combine: local AlgoDSA-only counts + LC API counts + GFG API counts
    # LC/GFG API counts already represent the full profile, so we add them.
    # For local counts, only include non-synced problems to avoid double-counting.
    local_only_easy = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='easy', is_leetcode_synced=False
    ).values('problem').distinct().count()
    local_only_medium = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='medium', is_leetcode_synced=False
    ).values('problem').distinct().count()
    local_only_hard = Submission.objects.filter(
        user=user, status='accepted', problem__difficulty='hard', is_leetcode_synced=False
    ).values('problem').distinct().count()

    easy_solved = local_only_easy + analytics.get('lc_easy', 0) + analytics.get('gfg_easy', 0)
    medium_solved = local_only_medium + analytics.get('lc_medium', 0) + analytics.get('gfg_medium', 0)
    hard_solved = local_only_hard + analytics.get('lc_hard', 0) + analytics.get('gfg_hard', 0)

    # AI Tutor Morning Standup & Readiness Analytics
    from apps.tutor.services.ai import AIService
    ai_service = AIService()
    morning_standup = ai_service.generate_morning_standup(user)

    # Readiness Scores across categories (Feature 9)
    readiness_scores = [
        {'name': 'Arrays', 'score': min(100, int(completion_pct * 1.2 + 20)), 'color': '#6366f1'},
        {'name': 'Strings', 'score': min(100, int(completion_pct * 1.1 + 15)), 'color': '#06b6d4'},
        {'name': 'Linked Lists', 'score': min(100, int(completion_pct * 0.9 + 10)), 'color': '#10b981'},
        {'name': 'Trees', 'score': min(100, int(completion_pct * 0.8 + 5)), 'color': '#eab308'},
        {'name': 'Graphs', 'score': min(100, int(completion_pct * 0.7)), 'color': '#a855f7'},
        {'name': 'DP', 'score': min(100, int(completion_pct * 0.6)), 'color': '#f43f5e'},
        {'name': 'Greedy', 'score': min(100, int(completion_pct * 0.85 + 10)), 'color': '#f97316'},
        {'name': 'Heap', 'score': min(100, int(completion_pct * 0.75 + 5)), 'color': '#3b82f6'},
    ]

    # Daily Micro-Drill Question (Feature 7)
    micro_drill = {
        'id': 1,
        'title': 'Spot the Bug: Sliding Window Pointer Bounds',
        'question': 'When `current_sum > target` in a positive integer array, which action restores the valid window condition?',
        'options': [
            {'key': 'opt1', 'text': 'Increment `right` pointer to expand window'},
            {'key': 'correct', 'text': 'Increment `left` pointer to shrink window'},
            {'key': 'opt3', 'text': 'Reset both `left` and `right` to index 0'}
        ]
    }

    # Spaced Repetition Due Queue (Feature 16)
    due_reviews = PatternMastery.objects.filter(user=user).order_by('mastery_score')[:5]

    context = {
        'analytics': analytics,
        'masteries': masteries,
        'topic_progresses': topic_progresses,
        'recommended': recommended,
        'weakest': weakest,
        'recent_activity': recent_activity,
        'total_problems': total_problems,
        'accepted_count': accepted_count,
        'leetcode_synced_count': leetcode_synced_count,
        'remaining_count': remaining_count,
        'completion_pct': completion_pct,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'daily_activity': list(daily_activity),
        'morning_standup': morning_standup,
        'readiness_scores': readiness_scores,
        'micro_drill': micro_drill,
        'due_reviews': due_reviews,
    }
    return render(request, 'dashboard/dashboard.html', context)


def _group_recent_activity(submissions, max_entries=10):
    """
    Group consecutive submissions for the same problem into single entries.
    Returns a list of dicts: {problem, attempts, solved, status_icon, latest_sub, difficulty}.
    """
    if not submissions:
        return []

    grouped = []
    current_group = None

    for sub in submissions:
        if current_group and current_group['problem_id'] == sub.problem_id:
            # Same problem — merge into current group
            current_group['attempts'] += 1
            if sub.status == 'accepted':
                current_group['solved'] = True
        else:
            # Different problem — save previous group and start new
            if current_group:
                grouped.append(current_group)
                if len(grouped) >= max_entries:
                    break
            current_group = {
                'problem_id': sub.problem_id,
                'problem': sub.problem,
                'attempts': 1,
                'solved': sub.status == 'accepted',
                'latest_sub': sub,
                'status_icon': sub.status_icon,
            }

    # Don't forget the last group
    if current_group and len(grouped) < max_entries:
        grouped.append(current_group)

    # Fix status icons for groups
    for entry in grouped:
        if entry['solved']:
            entry['status_icon'] = '✅'
            if entry['attempts'] > 1:
                entry['summary'] = f"{entry['attempts']} attempts, solved"
            else:
                entry['summary'] = 'Solved'
        else:
            entry['status_icon'] = '❌'
            entry['summary'] = f"{entry['attempts']} attempt{'s' if entry['attempts'] > 1 else ''}, unsolved"

    return grouped


@login_required
@require_POST
def sync_leetcode_view(request):
    """POST endpoint to trigger LeetCode sync for current user."""
    username = request.POST.get('leetcode_username') or request.user.leetcode_username

    if not username:
        messages.error(request, 'Please provide a LeetCode username in your profile settings.')
        return redirect('profile')

    service = LeetCodeSyncService(username)
    result = service.sync_user(request.user)

    if result.get('success'):
        new_cnt = result.get('newly_synced_count', 0)
        messages.success(
            request,
            f'Synced with LeetCode (@{username})! Imported {new_cnt} new solved problems.'
        )
    else:
        messages.error(request, f'LeetCode Sync Error: {result.get("error")}')

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse(result)

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
@require_POST
def sync_gfg_view(request):
    """POST endpoint to trigger GeeksforGeeks sync for current user."""
    username = request.POST.get('gfg_username') or request.user.gfg_username
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'

    if not username:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'No GeeksforGeeks handle configured.'})
        messages.error(request, 'Please provide a GeeksforGeeks handle in your profile settings.')
        return redirect('profile')

    service = GFGSyncService(username)
    result = service.sync_user(request.user)

    if result.get('success'):
        total = result.get('total_solved_gfg', 0)
        if total == 0:
            result['warning'] = 'Sync completed but returned 0 solved problems. The GFG profile may be private or the username may be incorrect.'
        messages.success(
            request,
            f'Synced with GeeksforGeeks (@{username})! Total Solved: {total}'
        )
    else:
        messages.error(request, f'GeeksforGeeks Sync Error: {result.get("error")}')

    if is_ajax:
        return JsonResponse(result)

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


@login_required
@require_POST
def sync_all_platforms_view(request):
    """1-Click Sync for both LeetCode and GeeksforGeeks."""
    lc_username = request.POST.get('leetcode_username') or request.user.leetcode_username
    gfg_username = request.POST.get('gfg_username') or request.user.gfg_username
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json'

    synced_any = False
    messages_list = []
    errors_list = []

    if lc_username:
        lc_service = LeetCodeSyncService(lc_username)
        res_lc = lc_service.sync_user(request.user)
        if res_lc.get('success'):
            synced_any = True
            messages_list.append(f"LeetCode (@{lc_username}): {res_lc.get('total_solved_leetcode')} solved")
        else:
            errors_list.append(f"LeetCode: {res_lc.get('error', 'Unknown error')}")

    if gfg_username:
        gfg_service = GFGSyncService(gfg_username)
        res_gfg = gfg_service.sync_user(request.user)
        if res_gfg.get('success'):
            synced_any = True
            messages_list.append(f"GeeksforGeeks (@{gfg_username}): {res_gfg.get('total_solved_gfg')} solved")
        else:
            errors_list.append(f"GFG: {res_gfg.get('error', 'Unknown error')}")

    if synced_any:
        messages.success(request, f"Multi-Platform Sync Complete! { ' | '.join(messages_list) }")
    elif not lc_username and not gfg_username:
        messages.warning(request, "No connected platform accounts found. Please add your LeetCode or GFG username.")
    else:
        messages.error(request, f"Sync failed: { ' | '.join(errors_list) }")

    if is_ajax:
        return JsonResponse({
            'success': synced_any,
            'messages': messages_list,
            'errors': errors_list,
        })

    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))


