from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import json
from .models import Topic, Problem, Hint
from .services.tracer import generate_trace



@login_required
def topic_list(request):
    """List all DSA topics (delegates to the redesigned learn_hub_view)."""
    return learn_hub_view(request)



@login_required
def problem_list(request, topic_slug):
    """List problems for a specific topic with filter options & per-topic difficulty breakdown."""
    from django.shortcuts import redirect
    if topic_slug.lower() in ['learn', 'hub', 'learn_hub', 'index', 'courses']:
        return redirect('learn_hub')

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
    """University Learning Hub Home Page with categorized topics and roadmap tree."""
    from .models import Topic, Lesson, VideoResource
    import re, json
    from apps.submissions.models import Submission
    from apps.progress.models import PatternMastery, SM2ReviewSchedule
    from django.utils import timezone

    user = request.user
    topics = Topic.objects.all().prefetch_related('patterns', 'lessons', 'problems').order_by('order')

    # Categories grouping
    categories = [
        {'key': 'foundations', 'title': 'Foundations', 'icon': '📐', 'desc': 'Big-O, Memory, Recursion'},
        {'key': 'linear', 'title': 'Linear Data Structures', 'icon': '📊', 'desc': 'Arrays, Strings, Hash Maps, Lists'},
        {'key': 'algorithms', 'title': 'Searching & Algorithmic Techniques', 'icon': '⚡', 'desc': 'Binary Search, Two Pointer, Sliding Window'},
        {'key': 'non_linear', 'title': 'Non-Linear Data Structures', 'icon': '🌳', 'desc': 'Trees, BST, Heap, Trie, Graph'},
        {'key': 'advanced', 'title': 'Advanced Data Structures & DP', 'icon': '🧩', 'desc': 'Dynamic Programming, Segment Trees'},
        {'key': 'math_bit', 'title': 'Math & Bit Manipulation', 'icon': '🔢', 'desc': 'Bitwise Tricks, Prime Sieve, GCD'},
    ]

    # User progress
    accepted_ids = set(Submission.objects.filter(
        user=user, status='accepted'
    ).values_list('problem_id', flat=True))

    total_problems = Problem.objects.filter(is_active=True).count()
    total_solved = len(accepted_ids)
    overall_progress = int((total_solved / total_problems * 100) if total_problems > 0 else 0)

    # Due SM-2 reviews
    today = timezone.now().date()
    due_reviews = SM2ReviewSchedule.objects.filter(user=user, next_review__lte=today).count()

    categorized_topics = []
    search_index = []

    for cat in categories:
        cat_topics = [t for t in topics if t.category == cat['key'] or (cat['key'] == 'linear' and not t.category)]
        topic_items = []
        for t in cat_topics:
            t_probs = t.problems.filter(is_active=True)
            t_solved = sum(1 for p in t_probs if p.id in accepted_ids)
            t_total = t_probs.count()
            t_pct = int((t_solved / t_total * 100) if t_total > 0 else 0)

            patterns = list(t.patterns.all())
            lessons = list(t.lessons.all())

            # Sub-concepts options
            sub_concepts = [
                {'name': 'Introduction & Memory', 'icon': '📖', 'url': f'/learn/{t.slug}/#sec-overview'},
                {'name': 'Core Logic & Strategy', 'icon': '💡', 'url': f'/learn/{t.slug}/#sec-logic'},
                {'name': 'Big-O Complexity Matrix', 'icon': '📈', 'url': f'/learn/{t.slug}/#sec-complexity'},
                {'name': 'Operations & Code (6 Languages)', 'icon': '💻', 'url': f'/learn/{t.slug}/#sec-code'},
                {'name': 'Common Mistakes & Gotchas', 'icon': '⚠️', 'url': f'/learn/{t.slug}/#sec-gotchas'},
                {'name': 'Things to Remember & Hacks', 'icon': '📌', 'url': f'/learn/{t.slug}/#sec-remember'},
                {'name': 'Interview Questions (5 Tiers)', 'icon': '🧠', 'url': f'/learn/{t.slug}/#sec-practice'},
            ]

            # Primary keywords
            t_kw = [t.name.lower(), t.slug.lower(), t.description.lower(), cat['title'].lower(), 'introduction', 'logic', 'complexity', 'operations', 'common mistakes', 'remember', 'interview', 'questions']

            # Topic specific keywords expansion (singular + plural + aliases)
            if t.slug in ['arrays', 'array']:
                t_kw.extend(['array', 'arrays', 'prefix sum', 'difference array', 'sliding window', 'two pointer', 'two pointers', 'kadane', 'subarrays', 'insertion', 'deletion', 'access', 'vector'])
            elif t.slug in ['strings', 'string']:
                t_kw.extend(['string', 'strings', 'frequency hash map', 'anagrams', 'palindromes', 'kmp', 'z-algorithm', 'string manipulation', 'pattern matching'])
            elif t.slug in ['sliding-window', 'sliding_window']:
                t_kw.extend(['sliding window', 'sliding', 'window', 'fixed window', 'variable window', 'subarray sum', 'max sum', 'min window'])
            elif t.slug in ['two-pointer', 'two_pointer', 'two-pointers']:
                t_kw.extend(['two pointer', 'two pointers', 'pointers', 'opposite direction', 'same direction', 'slow fast pointers', 'container with most water', '3sum'])
            elif t.slug in ['binary-search', 'binary_search']:
                t_kw.extend(['binary search', 'binary', 'search', 'logarithmic search', 'lower bound', 'upper bound', 'rotated sorted array', 'binary search on answer'])
            elif t.slug in ['linked-list', 'linked_list']:
                t_kw.extend(['linked list', 'linked', 'list', 'lists', 'pointers', 'dummy node', 'slow fast pointers', 'floyd cycle', 'reversal'])
            elif t.slug in ['stack']:
                t_kw.extend(['stack', 'stacks', 'lifo', 'valid parentheses', 'monotonic stack', 'next greater element'])
            elif t.slug in ['queue']:
                t_kw.extend(['queue', 'queues', 'fifo', 'deque', 'monotonic queue', 'sliding window max'])
            elif t.slug in ['trees', 'tree']:
                t_kw.extend(['tree', 'trees', 'binary tree', 'dfs', 'bfs', 'inorder', 'preorder', 'postorder', 'height', 'diameter', 'lca'])
            elif t.slug in ['bst']:
                t_kw.extend(['bst', 'binary search tree', 'inorder sorted', 'validate bst', 'kth smallest'])
            elif t.slug in ['heap']:
                t_kw.extend(['heap', 'heaps', 'priority queue', 'min heap', 'max heap', 'top k elements', 'median stream'])
            elif t.slug in ['trie']:
                t_kw.extend(['trie', 'tries', 'prefix tree', 'autocomplete', 'word search'])
            elif t.slug in ['graph', 'graphs']:
                t_kw.extend(['graph', 'graphs', 'bfs', 'dfs', 'adjacency list', 'topological sort', 'dijkstra', 'dsu', 'connected components'])
            elif t.slug in ['greedy']:
                t_kw.extend(['greedy', 'interval scheduling', 'activity selection', 'fractional knapsack', 'jump game'])
            elif t.slug in ['backtracking']:
                t_kw.extend(['backtracking', 'subsets', 'combinations', 'permutations', 'n-queens', 'sudoku solver'])
            elif t.slug in ['dynamic-programming', 'dp']:
                t_kw.extend(['dynamic programming', 'dp', 'memoization', 'tabulation', '0/1 knapsack', 'lcs', 'subproblems'])
            elif t.slug in ['segment-tree']:
                t_kw.extend(['segment tree', 'segment', 'range query', 'point update', 'lazy propagation'])
            elif t.slug in ['fenwick-tree']:
                t_kw.extend(['fenwick tree', 'fenwick', 'bit', 'binary indexed tree', 'prefix sum query'])
            elif t.slug in ['bit-manipulation', 'bit']:
                t_kw.extend(['bit manipulation', 'bit', 'bitwise', 'binary', 'xor', 'single number', 'kernighan', 'bitmask'])
            elif t.slug in ['math', 'mathematics']:
                t_kw.extend(['math', 'mathematics', 'number theory', 'prime sieve', 'gcd', 'euclidean', 'exponentiation', 'modular arithmetic', 'prime', 'primes', 'bit math'])

            # Extract pure alphanumeric lowercase words to avoid HTML entity encoding bugs
            clean_text = re.sub(r'[^a-zA-Z0-9\s]', ' ', ' '.join(t_kw)).lower()
            raw_words = [w for w in clean_text.split() if len(w) > 1]
            search_keywords_str = ' '.join(set(raw_words))

            # 1. Main Topic Entry in Search Index
            search_index.append({
                'type': 'topic',
                'title': f"{t.name} (Full Workspace)",
                'parent_topic': cat['title'],
                'icon': t.icon or '📊',
                'keywords': search_keywords_str,
                'url': f'/learn/{t.slug}/'
            })

            # 2. Add Sub-part learning options for this topic in Search Index
            topic_options = [
                ('📖 Overview & Real-World Intuition', f'/learn/{t.slug}/#sec-overview', f"{t.name} overview intuition real world daily life analogy"),
                ('💡 Core Logic & Algorithm Strategy', f'/learn/{t.slug}/#sec-logic', f"{t.name} logic core strategy algorithm approach"),
                ('📈 Time & Space Complexity (Big-O)', f'/learn/{t.slug}/#sec-complexity', f"{t.name} complexity time space big-o best average worst space complexity"),
                ('💻 Operations Performed (6 Languages)', f'/learn/{t.slug}/#sec-code', f"{t.name} operations python cpp java js go rust code insert delete access search"),
                ('⚠️ Common Mistakes in Data Structures', f'/learn/{t.slug}/#sec-gotchas', f"{t.name} common mistakes gotchas pitfalls off by one overflow"),
                ('📌 Things to Remember & FAANG Hacks', f'/learn/{t.slug}/#sec-remember', f"{t.name} things to remember faang interview tips tricks hacks"),
                ('🧠 Interview Questions (5 Tiers)', f'/learn/{t.slug}/#sec-practice', f"{t.name} interview questions practice concept pattern mastery expert easy medium hard"),
            ]

            def clean_kw(str_input):
                return ' '.join(set([w for w in re.sub(r'[^a-zA-Z0-9\s]', ' ', str_input).lower().split() if len(w) > 1]))

            for opt_title, opt_url, opt_kw in topic_options:
                search_index.append({
                    'type': 'subconcept',
                    'title': f"{t.name} — {opt_title}",
                    'parent_topic': t.name,
                    'icon': t.icon or '📚',
                    'keywords': clean_kw(f"{opt_kw} {' '.join(t_kw)}"),
                    'url': opt_url
                })

            # 3. Add Sub-Patterns & Lessons
            for p in patterns:
                t_kw.append(p.name.lower())
                sub_concepts.append({
                    'name': p.name,
                    'icon': p.icon or '⚡',
                    'url': f'/learn/{t.slug}/{p.slug}/'
                })
                search_index.append({
                    'type': 'pattern',
                    'title': f"{p.name} Pattern",
                    'parent_topic': t.name,
                    'icon': p.icon or '⚡',
                    'keywords': clean_kw(f"{p.name} {p.slug} {t.name} {' '.join(t_kw)}"),
                    'url': f'/learn/{t.slug}/{p.slug}/'
                })

            for l in lessons:
                t_kw.append(l.title.lower())
                p_slug = l.pattern.slug if l.pattern else (patterns[0].slug if patterns else '')
                p_name = l.pattern.name if l.pattern else ''
                if p_slug:
                    sub_concepts.append({
                        'name': l.title,
                        'icon': '📖',
                        'url': f'/learn/{t.slug}/{p_slug}/{l.slug}/'
                    })
                    search_index.append({
                        'type': 'lesson',
                        'title': f"Lesson: {l.title}",
                        'parent_topic': t.name,
                        'icon': '📖',
                        'keywords': clean_kw(f"{l.title} {l.slug} {p_name} {t.name} {l.overview} {' '.join(t_kw)}"),
                        'url': f'/learn/{t.slug}/{p_slug}/{l.slug}/'
                    })

            search_keywords_str = ' '.join(set(t_kw))

            four_pillars = [
                {'name': 'Notes & Theory', 'icon': '📖', 'url': f'/learn/{t.slug}/#sec-overview', 'badge': 'Theory'},
                {'name': 'Cheatsheets & Big-O', 'icon': '⚡', 'url': f'/learn/{t.slug}/#sec-complexity', 'badge': 'Matrix'},
                {'name': 'Interview Questions', 'icon': '🧠', 'url': f'/learn/{t.slug}/#sec-practice', 'badge': f"{t_total} Qs"},
                {'name': 'Common Mistakes', 'icon': '⚠️', 'url': f'/learn/{t.slug}/#sec-gotchas', 'badge': 'Gotchas'},
            ]

            topic_items.append({
                'topic': t,
                'solved_count': t_solved,
                'total_count': t_total,
                'progress_pct': t_pct,
                'lesson_count': len(lessons) or len(patterns) or 1,
                'sub_concepts': sub_concepts,
                'four_pillars': four_pillars,
                'search_text': search_keywords_str
            })

        categorized_topics.append({
            'info': cat,
            'topics': topic_items
        })

    # Fetch last submitted problem or studied topic for Continue Learning
    last_sub = Submission.objects.filter(user=user).select_related('problem__topic').order_by('-created_at').first()
    continue_learning = None
    if last_sub and last_sub.problem and last_sub.problem.topic:
        t = last_sub.problem.topic
        t_probs = t.problems.filter(is_active=True)
        t_solved = sum(1 for p in t_probs if p.id in accepted_ids)
        t_total = t_probs.count()
        t_pct = int((t_solved / t_total * 100) if t_total > 0 else 0)
        continue_learning = {
            'topic': t,
            'last_problem': last_sub.problem,
            'solved_count': t_solved,
            'total_count': t_total,
            'progress_pct': t_pct,
            'url': f'/learn/{t.slug}/'
        }
    else:
        arrays_topic = Topic.objects.filter(slug='arrays').first()
        if arrays_topic:
            t_probs = arrays_topic.problems.filter(is_active=True)
            t_solved = sum(1 for p in t_probs if p.id in accepted_ids)
            t_total = t_probs.count()
            t_pct = int((t_solved / t_total * 100) if t_total > 0 else 0)
            continue_learning = {
                'topic': arrays_topic,
                'last_problem': t_probs.first(),
                'solved_count': t_solved,
                'total_count': t_total,
                'progress_pct': t_pct,
                'url': f'/learn/{arrays_topic.slug}/'
            }

    # Recommended next track
    recommended_topic = Topic.objects.filter(slug='sliding-window').first() or topics.first()

    # Ecosystem statistics
    statistics = {
        'total_topics': topics.count(),
        'total_lessons': sum(t.lessons.count() or t.patterns.count() or 1 for t in topics),
        'total_problems': total_problems,
        'total_solved': total_solved,
        'overall_progress': overall_progress,
        'user_streak': getattr(user, 'streak', 1),
        'due_reviews': due_reviews
    }

    import json
    context = {
        'categorized_topics': categorized_topics,
        'topics': topics,
        'search_index_json': json.dumps(search_index),
        'total_problems': total_problems,
        'total_solved': total_solved,
        'overall_progress': overall_progress,
        'due_reviews_count': due_reviews,
        'user_streak': getattr(user, 'streak', 1),
        'continue_learning': continue_learning,
        'recommended_topic': recommended_topic,
        'statistics': statistics
    }
    return render(request, 'problems/learn_hub.html', context)


@login_required
def global_search_api(request):
    """
    Global Search API Endpoint (/api/search/?q=...)
    Searches across Topic, Pattern, Lesson, Problem models and returns categorized JSON.
    """
    from django.db.models import Q
    from .models import Topic, Pattern, Lesson, Problem

    query = request.GET.get('q', '').strip()
    if not query or len(query) < 2:
        return JsonResponse({'results': []})

    results = []

    # 1. Topic Matches
    topics = Topic.objects.filter(
        Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query) | Q(notes_content__icontains=query)
    )[:6]
    for t in topics:
        results.append({
            'type': 'topic',
            'title': f"{t.name} Track",
            'slug': t.slug,
            'parent': t.get_category_display() if hasattr(t, 'get_category_display') else t.category,
            'icon': t.icon or '📊',
            'desc': t.description[:90] if t.description else f"{t.name} DSA Track",
            'url': f'/learn/{t.slug}/'
        })

    # 2. Pattern Matches
    patterns = Pattern.objects.filter(
        Q(name__icontains=query) | Q(slug__icontains=query) | Q(description__icontains=query)
    ).select_related('topic')[:6]
    for p in patterns:
        results.append({
            'type': 'pattern',
            'title': f"{p.name} Pattern",
            'slug': p.slug,
            'parent': p.topic.name,
            'icon': p.icon or '⚡',
            'desc': p.description[:90] if p.description else f"Pattern in {p.topic.name}",
            'url': f'/learn/{p.topic.slug}/{p.slug}/'
        })

    # 3. Lesson Matches
    lessons = Lesson.objects.filter(
        Q(title__icontains=query) | Q(slug__icontains=query) | Q(overview__icontains=query) | Q(when_use__icontains=query)
    ).select_related('topic', 'pattern')[:6]
    for l in lessons:
        p_slug = l.pattern.slug if l.pattern else ''
        url = f'/learn/{l.topic.slug}/{p_slug}/{l.slug}/' if p_slug else f'/learn/{l.topic.slug}/'
        results.append({
            'type': 'lesson',
            'title': l.title,
            'slug': l.slug,
            'parent': l.topic.name,
            'icon': '📖',
            'desc': l.overview[:90] if l.overview else f"Lesson in {l.topic.name}",
            'url': url
        })

    # 4. Problem Matches
    problems = Problem.objects.filter(
        Q(title__icontains=query) | Q(slug__icontains=query) | Q(difficulty__icontains=query)
    ).select_related('topic')[:6]
    for pr in problems:
        t_slug = pr.topic.slug if pr.topic else 'arrays'
        results.append({
            'type': 'problem',
            'title': pr.title,
            'slug': pr.slug,
            'parent': pr.topic.name if pr.topic else 'DSA',
            'icon': '🎯',
            'desc': f"{pr.difficulty.capitalize()} Problem • Est: {pr.est_time_mins} mins",
            'url': f'/{t_slug}/{pr.slug}/'
        })

    return JsonResponse({'query': query, 'count': len(results), 'results': results})


@login_required
def learn_topic_view(request, topic_slug):
    """Topic University Course Page."""
    from django.shortcuts import redirect
    if topic_slug.lower() in ['learn', 'hub', 'learn_hub', 'index', 'courses']:
        return redirect('learn_hub')

    from .models import Topic, Lesson, VideoResource
    from apps.submissions.models import Submission

    topic = get_object_or_404(Topic.objects.prefetch_related('patterns', 'lessons', 'problems'), slug=topic_slug)
    user = request.user

    # Fetch patterns & lessons
    patterns = topic.patterns.prefetch_related('lessons').all()
    lessons = topic.lessons.all()
    if not lessons.exists() and patterns.exists():
        lessons = Lesson.objects.filter(pattern__in=patterns)

    # First lesson if exists
    active_lesson = lessons.first()

    accepted_ids = set(Submission.objects.filter(
        user=user, problem__topic=topic, status='accepted'
    ).values_list('problem_id', flat=True))

    problems = list(topic.problems.filter(is_active=True))

    # Categorize questions into 5 tiers
    tier_concept = [p for p in problems if p.practice_tier == 'concept_building' or p.difficulty == 'easy']
    tier_pattern = [p for p in problems if p.practice_tier == 'pattern_recognition' or p.difficulty == 'easy']
    tier_mastery = [p for p in problems if p.practice_tier == 'pattern_mastery' or p.difficulty == 'medium']
    tier_interview = [p for p in problems if p.practice_tier == 'interview_ready' or p.difficulty == 'medium']
    tier_expert = [p for p in problems if p.practice_tier == 'expert' or p.difficulty == 'hard']

    # Curated videos
    videos = VideoResource.objects.filter(topic=topic).order_by('order')

    all_topics = Topic.objects.all().prefetch_related('patterns', 'lessons').order_by('order')

    context = {
        'topic': topic,
        'patterns': patterns,
        'lessons': lessons,
        'active_lesson': active_lesson,
        'problems': problems,
        'accepted_ids': accepted_ids,
        'tier_concept': tier_concept,
        'tier_pattern': tier_pattern,
        'tier_mastery': tier_mastery,
        'tier_interview': tier_interview,
        'tier_expert': tier_expert,
        'videos': videos,
        'all_topics': all_topics,
    }
    return render(request, 'problems/learn_topic.html', context)


@login_required
def learn_pattern_view(request, topic_slug, pattern_slug):
    """Pattern / Subtopic Lesson View."""
    from .models import Topic, Pattern, Lesson, VideoResource
    from apps.submissions.models import Submission

    topic = get_object_or_404(Topic, slug=topic_slug)
    pattern = get_object_or_404(Pattern, topic=topic, slug=pattern_slug)

    lessons = pattern.lessons.all()
    active_lesson = lessons.first()

    videos = VideoResource.objects.filter(pattern=pattern).order_by('order')
    if not videos.exists():
        videos = VideoResource.objects.filter(topic=topic).order_by('order')

    problems = list(topic.problems.filter(is_active=True))
    accepted_ids = set(Submission.objects.filter(
        user=request.user, problem__topic=topic, status='accepted'
    ).values_list('problem_id', flat=True))

    all_topics = Topic.objects.all().prefetch_related('patterns', 'lessons').order_by('order')

    context = {
        'topic': topic,
        'pattern': pattern,
        'lessons': lessons,
        'active_lesson': active_lesson,
        'data': pattern.content_json,
        'videos': videos,
        'problems': problems,
        'accepted_ids': accepted_ids,
        'all_topics': all_topics,
    }
    return render(request, 'problems/learn_pattern.html', context)


@login_required
def learn_lesson_view(request, topic_slug, pattern_slug, lesson_slug):
    """Specific Lesson Detail View."""
    from .models import Topic, Pattern, Lesson, VideoResource
    from apps.submissions.models import Submission

    topic = get_object_or_404(Topic, slug=topic_slug)
    pattern = get_object_or_404(Pattern, topic=topic, slug=pattern_slug)
    lesson = get_object_or_404(Lesson, pattern=pattern, slug=lesson_slug)

    problems = list(topic.problems.filter(is_active=True))
    accepted_ids = set(Submission.objects.filter(
        user=request.user, problem__topic=topic, status='accepted'
    ).values_list('problem_id', flat=True))

    all_topics = Topic.objects.all().prefetch_related('patterns', 'lessons').order_by('order')

    patterns = topic.patterns.prefetch_related('lessons').all()
    lessons = topic.lessons.all()
    if not lessons.exists() and patterns.exists():
        lessons = Lesson.objects.filter(pattern__in=patterns)

    videos = lesson.video_resources.all()
    if not videos.exists():
        videos = VideoResource.objects.filter(topic=topic).order_by('order')

    tier_concept = [p for p in problems if p.practice_tier == 'concept_building' or p.difficulty == 'easy']
    tier_pattern = [p for p in problems if p.practice_tier == 'pattern_recognition' or p.difficulty == 'easy']
    tier_mastery = [p for p in problems if p.practice_tier == 'pattern_mastery' or p.difficulty == 'medium']
    tier_interview = [p for p in problems if p.practice_tier == 'interview_ready' or p.difficulty == 'medium']
    tier_expert = [p for p in problems if p.practice_tier == 'expert' or p.difficulty == 'hard']

    context = {
        'topic': topic,
        'pattern': pattern,
        'patterns': patterns,
        'lessons': lessons,
        'lesson': lesson,
        'active_lesson': lesson,
        'videos': videos,
        'problems': problems,
        'accepted_ids': accepted_ids,
        'tier_concept': tier_concept,
        'tier_pattern': tier_pattern,
        'tier_mastery': tier_mastery,
        'tier_interview': tier_interview,
        'tier_expert': tier_expert,
        'all_topics': all_topics,
    }
    return render(request, 'problems/learn_topic.html', context)


@login_required
def record_sm2_review(request):
    """API endpoint to update SM-2 Spaced Repetition for a topic/pattern/lesson."""
    from apps.progress.models import SM2ReviewSchedule
    from django.utils import timezone
    import datetime
    import json

    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            days = int(data.get('days', 1))
            topic_id = data.get('topic_id')

            topic = get_object_or_404(Topic, id=topic_id) if topic_id else None

            next_date = timezone.now().date() + datetime.timedelta(days=days)
            schedule, created = SM2ReviewSchedule.objects.update_or_create(
                user=request.user,
                topic=topic,
                defaults={
                    'interval_days': days,
                    'next_review': next_date,
                    'repetitions': 1 if days <= 3 else 2
                }
            )

            return JsonResponse({
                'status': 'success',
                'message': f'Review scheduled in {days} days ({next_date.strftime("%b %d, %Y")})',
                'next_review': str(next_date)
            })
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)




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
def visual_execution_lab(request):
    """AI Visual Code Execution Lab — Step-by-Step Educational Execution Engine."""
    return render(request, 'lab/execution_lab.html')


@login_required
def api_generate_trace(request):
    """API endpoint to generate an execution trace for the AI Code Lab without blocking the browser."""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            code = data.get('code', '')
            language = data.get('language', 'python')

            trace_result = generate_trace(code, language)
            return JsonResponse(trace_result)
        except Exception as e:
            return JsonResponse({'error': f"Failed to generate trace: {str(e)}"}, status=500)
    return JsonResponse({'error': 'Method not allowed'}, status=405)



@login_required
def mock_interview(request):
    """FAANG AI Mock Interviewer Workstation (Feature: Interview Mode)."""
    problem_id = request.GET.get('problem_id')
    problem = None
    if problem_id:
        problem = Problem.objects.filter(id=problem_id, is_active=True).first()
    if not problem:
        problem = Problem.objects.filter(is_active=True).first()

    all_problems = list(Problem.objects.filter(is_active=True).select_related('topic')[:12])
    sample_cases = list(problem.test_cases.filter(is_sample=True)) if problem else []
    hints = list(problem.hints.all().order_by('level')) if problem else []

    context = {
        'problem': problem,
        'all_problems': all_problems,
        'sample_cases': sample_cases,
        'hints': hints,
        'time_limit_mins': 45,
    }
    return render(request, 'problems/interview.html', context)


