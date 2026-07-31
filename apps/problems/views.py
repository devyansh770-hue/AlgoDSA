from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Topic, Problem, Hint


@login_required
def topic_list(request):
    """List all DSA topics with comprehensive analytics, learning paths & recommendations."""
    topics = Topic.objects.all()
    user = request.user

    from apps.submissions.models import Submission
    from apps.progress.services.spaced_repetition import get_recommended_problems
    from apps.progress.models import PatternMastery

    # Masteries & Weakest Pattern
    masteries = PatternMastery.objects.filter(user=user).order_by('mastery_score')
    weakest = masteries.first() if masteries.exists() else None

    # Total stats
    total_problems_count = Problem.objects.filter(is_active=True).count()
    accepted_problem_ids = set(Submission.objects.filter(
        user=user, status='accepted'
    ).values_list('problem_id', flat=True))

    total_solved_count = len(accepted_problem_ids)
    overall_progress_pct = int((total_solved_count / total_problems_count * 100) if total_problems_count > 0 else 0)

    # Map Topic Lucide Icons
    topic_lucide_map = {
        'arrays': 'layers',
        'strings': 'type',
        'linked-lists': 'link',
        'trees': 'tree-deciduous',
        'graphs': 'network',
        'dynamic-programming': 'cpu',
        'two-pointers': 'move-horizontal',
        'sliding-window': 'box',
        'stack-queue': 'rows',
    }

    # Calculate progress per topic for the current user
    topic_data = []
    topics_completed_count = 0

    for topic in topics:
        topic_problems = topic.problems.filter(is_active=True)
        total = topic_problems.count()
        solved = sum(1 for p in topic_problems if p.id in accepted_problem_ids)
        progress = int((solved / total * 100) if total > 0 else 0)

        if total > 0 and solved == total:
            topics_completed_count += 1

        # Difficulty breakdown per topic
        easy_cnt = topic_problems.filter(difficulty='easy').count()
        med_cnt = topic_problems.filter(difficulty='medium').count()
        hard_cnt = topic_problems.filter(difficulty='hard').count()

        # Mastery status text & styling
        if progress == 0:
            mastery_level = 'Unstarted'
            mastery_badge = 'badge-pattern'
            mastery_color = 'var(--text-muted)'
            mastery_stars = '☆☆☆☆☆'
        elif progress < 40:
            mastery_level = 'Beginner'
            mastery_badge = 'badge-medium'
            mastery_color = 'var(--mastery-weak)'
            mastery_stars = '★☆☆☆☆'
        elif progress < 75:
            mastery_level = 'Intermediate'
            mastery_badge = 'badge-medium'
            mastery_color = 'var(--mastery-medium)'
            mastery_stars = '★★★☆☆'
        elif progress < 100:
            mastery_level = 'Advanced'
            mastery_badge = 'badge-easy'
            mastery_color = 'var(--stat-primary)'
            mastery_stars = '★★★★☆'
        else:
            mastery_level = 'Mastered'
            mastery_badge = 'badge-easy'
            mastery_color = 'var(--mastery-strong)'
            mastery_stars = '★★★★★'

        # Progress bar color token rule
        if progress <= 30:
            bar_color = 'var(--mastery-weak)'
        elif progress <= 60:
            bar_color = 'var(--mastery-medium)'
        elif progress <= 85:
            bar_color = 'var(--stat-primary)'
        else:
            bar_color = 'var(--mastery-strong)'

        topic_data.append({
            'topic': topic,
            'lucide_icon': topic_lucide_map.get(topic.slug, 'book-open'),
            'total': total,
            'solved': solved,
            'remaining': max(0, total - solved),
            'progress': progress,
            'bar_color': bar_color,
            'easy_cnt': easy_cnt,
            'med_cnt': med_cnt,
            'hard_cnt': hard_cnt,
            'mastery_level': mastery_level,
            'mastery_badge': mastery_badge,
            'mastery_color': mastery_color,
            'mastery_stars': mastery_stars,
            'patterns_count': topic.patterns.count(),
        })

    # Recommended problems
    recommended = get_recommended_problems(user, limit=4)

    # Continue Learning Current Topic (First in-progress topic)
    current_topic_item = next((td for td in topic_data if td['progress'] > 0 and td['progress'] < 100), None)
    if not current_topic_item and topic_data:
        current_topic_item = topic_data[0]

    context = {
        'topic_data': topic_data,
        'total_problems_count': total_problems_count,
        'total_solved_count': total_solved_count,
        'overall_progress_pct': overall_progress_pct,
        'topics_completed_count': topics_completed_count,
        'total_topics_count': len(topic_data),
        'weakest': weakest,
        'recommended': recommended,
        'current_topic_item': current_topic_item,
        'user_streak': user.streak,
    }
    return render(request, 'problems/topic_list.html', context)


@login_required
def problem_list(request, topic_slug):
    """List problems for a specific topic with filter options & per-topic difficulty breakdown."""
    topic = get_object_or_404(Topic, slug=topic_slug)
    problems = topic.problems.filter(is_active=True)

    filter_type = request.GET.get('filter', 'all')  # 'all', 'solved', 'remaining'

    # Get solved status map (local vs leetcode)
    from apps.submissions.models import Submission
    accepted_submissions = Submission.objects.filter(
        user=request.user,
        problem__topic=topic,
        status='accepted'
    ).select_related('problem')

    solved_set = set()
    leetcode_synced_set = set()

    for sub in accepted_submissions:
        solved_set.add(sub.problem_id)
        if sub.is_leetcode_synced:
            leetcode_synced_set.add(sub.problem_id)

    # Calculate Easy, Medium, Hard breakdown
    easy_total = problems.filter(difficulty='easy').count()
    medium_total = problems.filter(difficulty='medium').count()
    hard_total = problems.filter(difficulty='hard').count()

    easy_solved = sum(1 for p in problems if p.difficulty == 'easy' and p.id in solved_set)
    medium_solved = sum(1 for p in problems if p.difficulty == 'medium' and p.id in solved_set)
    hard_solved = sum(1 for p in problems if p.difficulty == 'hard' and p.id in solved_set)

    total_count = problems.count()
    solved_count = len(solved_set)
    topic_progress_pct = int((solved_count / total_count * 100) if total_count > 0 else 0)

    easy_pct = int((easy_solved / easy_total * 100) if easy_total > 0 else 0)
    medium_pct = int((medium_solved / medium_total * 100) if medium_total > 0 else 0)
    hard_pct = int((hard_solved / hard_total * 100) if hard_total > 0 else 0)

    problem_data = []
    all_problems_list = list(problems)

    for idx, problem in enumerate(all_problems_list):
        is_solved = problem.id in solved_set
        is_lc = problem.id in leetcode_synced_set

        # Filter check
        if filter_type == 'solved' and not is_solved:
            continue
        elif filter_type == 'remaining' and is_solved:
            continue

        # Status badge & style
        if is_solved:
            status_text = 'Solved'
            status_badge = 'badge-easy'
            status_card_class = 'solved-card'
        else:
            status_text = 'Not Started'
            status_badge = 'badge-pattern'
            status_card_class = 'unsolved-card'

        # Metadata mapping
        if problem.difficulty == 'easy':
            xp = 20
            est_time = '15 mins'
            acc_rate = '74%'
        elif problem.difficulty == 'medium':
            xp = 35
            est_time = '25 mins'
            acc_rate = '56%'
        else:
            xp = 50
            est_time = '40 mins'
            acc_rate = '38%'

        next_prob = all_problems_list[(idx + 1) % len(all_problems_list)] if len(all_problems_list) > 1 else None

        problem_data.append({
            'problem': problem,
            'solved': is_solved,
            'is_leetcode': is_lc,
            'status_text': status_text,
            'status_badge': status_badge,
            'status_card_class': status_card_class,
            'xp_reward': xp,
            'est_time': est_time,
            'acc_rate': acc_rate,
            'next_problem': next_prob,
        })

    context = {
        'topic': topic,
        'problem_data': problem_data,
        'filter_type': filter_type,
        'total_count': total_count,
        'solved_count': solved_count,
        'remaining_count': max(0, total_count - solved_count),
        'topic_progress_pct': topic_progress_pct,
        'easy_total': easy_total,
        'medium_total': medium_total,
        'hard_total': hard_total,
        'easy_solved': easy_solved,
        'medium_solved': medium_solved,
        'hard_solved': hard_solved,
        'easy_pct': easy_pct,
        'medium_pct': medium_pct,
        'hard_pct': hard_pct,
    }
    return render(request, 'problems/problem_list.html', context)


@login_required
def problem_detail(request, topic_slug, problem_slug):
    """Problem workspace page with Monaco editor."""
    topic = get_object_or_404(Topic, slug=topic_slug)
    problem = get_object_or_404(Problem, topic=topic, slug=problem_slug)

    # User's language preference
    lang = request.user.preferred_language or 'python'

    # Visible sample test cases
    sample_cases = problem.test_cases.filter(is_sample=True)

    # Check if user has solved this problem
    from apps.submissions.models import Submission
    is_solved = Submission.objects.filter(
        user=request.user, problem=problem, status='accepted'
    ).exists()

    # Editorial unlocked status
    editorial_unlocked = is_solved or False

    # Recent submissions for this problem
    recent_submissions = Submission.objects.filter(
        user=request.user, problem=problem
    ).order_by('-created_at')[:5]

    context = {
        'topic': topic,
        'problem': problem,
        'language': lang,
        'sample_cases': sample_cases,
        'is_solved': is_solved,
        'editorial_unlocked': editorial_unlocked,
        'recent_submissions': recent_submissions,
    }
    return render(request, 'problems/problem_detail.html', context)


@login_required
def learn_hub_view(request):
    """DSA Learning & Notes Hub Overview Page."""
    topics = Topic.objects.all().order_by('order')

    # Aggregated pattern stats for learning cards
    topic_data = []
    for topic in topics:
        total_p = topic.problems.filter(is_active=True).count()
        total_patterns = topic.patterns.count()
        topic_data.append({
            'topic': topic,
            'total_problems': total_p,
            'total_patterns': total_patterns,
        })

    context = {
        'topic_data': topic_data,
        'topics': topics,
    }
    return render(request, 'problems/learn_hub.html', context)


@login_required
def learn_topic_view(request, topic_slug):
    """Detailed Learning Guide & Custom Notes Page for a specific topic."""
    topic = get_object_or_404(Topic, slug=topic_slug)
    problems = topic.problems.filter(is_active=True)
    patterns = topic.patterns.all()

    # Calculate Easy, Medium, Hard breakdown
    easy_count = problems.filter(difficulty='easy').count()
    medium_count = problems.filter(difficulty='medium').count()
    hard_count = problems.filter(difficulty='hard').count()

    context = {
        'topic': topic,
        'problems': problems,
        'patterns': patterns,
        'easy_count': easy_count,
        'medium_count': medium_count,
        'hard_count': hard_count,
    }
    return render(request, 'problems/learn_topic.html', context)


@login_required
def learn_pattern_view(request, topic_slug, pattern_slug):
    """21-section comprehensive study guide for a specific pattern."""
    from .models import Pattern
    topic = get_object_or_404(Topic, slug=topic_slug)
    pattern = get_object_or_404(Pattern, topic=topic, slug=pattern_slug)
    
    # Also fetch some practice problems for this pattern if we wanted to
    # but the pattern data might just dictate the structure for now
    problems = topic.problems.filter(is_active=True) # Could filter by pattern if mapping exists
    
    context = {
        'topic': topic,
        'pattern': pattern,
        'data': pattern.content_json, # The 21 sections of JSON data
        'problems': problems
    }
    return render(request, 'problems/learn_pattern.html', context)



@login_required
def get_hint(request, problem_id, level):
    """Return a hint for the given problem and level."""
    problem = get_object_or_404(Problem, id=problem_id)
    hint = Hint.objects.filter(problem=problem, level=level).first()

    if hint:
        return JsonResponse({'hint': hint.content, 'level': level})
    return JsonResponse({'hint': 'No hint available for this level.', 'level': level})


@login_required
def get_starter_code(request, problem_id):
    """Return starter code for a specific language."""
    problem = get_object_or_404(Problem, id=problem_id)
    language = request.GET.get('language', 'python')
    code = problem.get_starter_code(language)
    return JsonResponse({'code': code, 'language': language})


@login_required
def algorithm_simulator(request):
    """Visual Algorithm Simulator with interactive step-by-step animations (Feature: Simulator)."""
    return render(request, 'simulator/simulator.html')


@login_required
def mock_interview(request):
    """FAANG AI Mock Interviewer Workstation (Feature: Interview Mode)."""
    problem = Problem.objects.filter(is_active=True).first()
    context = {
        'problem': problem,
        'time_limit_mins': 45,
    }
    return render(request, 'problems/interview.html', context)
