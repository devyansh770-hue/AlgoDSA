"""
Spaced Repetition service using the SM-2 algorithm.

This is an adaptation of the SuperMemo SM-2 algorithm used in Anki.
It schedules review of DSA patterns based on user performance.
"""
import math
from datetime import timedelta
from django.utils import timezone
from apps.progress.models import PatternMastery, TopicProgress


def update_mastery(user, problem, correct):
    """
    Update pattern mastery after a submission.

    Uses SM-2 algorithm to calculate next review date.

    Args:
        user: User instance
        problem: Problem instance
        correct: bool, whether the submission was accepted
    """
    mastery, created = PatternMastery.objects.get_or_create(
        user=user,
        pattern=problem.pattern,
        defaults={
            'next_review': timezone.now().date(),
        }
    )

    mastery.attempts += 1
    if correct:
        mastery.correct += 1

    # Calculate mastery score (weighted recent performance)
    if mastery.attempts > 0:
        mastery.mastery_score = round((mastery.correct / mastery.attempts) * 100, 1)

    # SM-2 Algorithm
    # Quality: 0-5 scale. 5 = perfect, 0 = complete failure
    quality = 5 if correct else 1

    if quality >= 3:
        # Correct response
        if mastery.repetitions == 0:
            mastery.interval_days = 1
        elif mastery.repetitions == 1:
            mastery.interval_days = 6
        else:
            mastery.interval_days = round(mastery.interval_days * mastery.ease_factor)

        mastery.repetitions += 1
    else:
        # Incorrect response — reset
        mastery.repetitions = 0
        mastery.interval_days = 1

    # Update ease factor
    mastery.ease_factor = max(
        1.3,
        mastery.ease_factor + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02))
    )

    # Set next review date
    mastery.next_review = timezone.now().date() + timedelta(days=mastery.interval_days)
    mastery.last_reviewed = timezone.now()
    mastery.save()

    # Update topic progress
    _update_topic_progress(user, problem)

    return mastery


def _update_topic_progress(user, problem):
    """Update topic progress after a submission."""
    from apps.submissions.models import Submission

    topic_progress, created = TopicProgress.objects.get_or_create(
        user=user,
        topic=problem.topic,
    )

    # Count distinct problems attempted and solved
    topic_progress.problems_attempted = Submission.objects.filter(
        user=user,
        problem__topic=problem.topic
    ).values('problem').distinct().count()

    topic_progress.problems_solved = Submission.objects.filter(
        user=user,
        problem__topic=problem.topic,
        status='accepted'
    ).values('problem').distinct().count()

    topic_progress.last_practiced = timezone.now()
    topic_progress.save()


def get_recommended_problems(user, limit=5):
    """
    Get problems recommended for the user based on spaced repetition.

    Priority:
    1. Weakest pattern (always gets at least 1-2 slots)
    2. Patterns due for review (next_review <= today)
    3. Other weak patterns
    4. Untouched patterns (no mastery record)
    """
    from apps.problems.models import Problem
    from apps.submissions.models import Submission

    today = timezone.now().date()
    recommended = []
    used_patterns = set()

    solved_ids = set(
        Submission.objects.filter(
            user=user,
            status='accepted'
        ).values_list('problem_id', flat=True)
    )

    def _add_problem_for_pattern(mastery, reason, max_to_add=1):
        """Helper: add unsolved problems for a pattern, return count added."""
        added = 0
        problems = Problem.objects.filter(
            pattern=mastery.pattern,
            is_active=True
        ).exclude(id__in=solved_ids)

        for p in problems:
            if len(recommended) >= limit or added >= max_to_add:
                break
            # Avoid duplicate problems
            if any(r['problem'].id == p.id for r in recommended):
                continue
            recommended.append({
                'problem': p,
                'reason': reason,
                'mastery': mastery,
            })
            added += 1
        return added

    # 1. Weakest pattern FIRST — guarantee at least 2 slots (or all available)
    weakest_mastery = PatternMastery.objects.filter(
        user=user
    ).order_by('mastery_score').first()

    if weakest_mastery:
        used_patterns.add(weakest_mastery.pattern)
        _add_problem_for_pattern(
            weakest_mastery,
            reason=f"Because you're weak in {weakest_mastery.pattern_display} ({weakest_mastery.mastery_score:.0f}% mastery)",
            max_to_add=2
        )

    # 2. Patterns due for review
    if len(recommended) < limit:
        due_patterns = PatternMastery.objects.filter(
            user=user,
            next_review__lte=today
        ).exclude(
            pattern__in=used_patterns
        ).order_by('mastery_score')

        for mastery in due_patterns:
            if len(recommended) >= limit:
                break
            used_patterns.add(mastery.pattern)
            _add_problem_for_pattern(
                mastery,
                reason=f"Due for review: {mastery.pattern_display} ({mastery.mastery_score:.0f}% mastery)",
            )

    # 3. Other weak patterns (not yet recommended)
    if len(recommended) < limit:
        weak_patterns = PatternMastery.objects.filter(
            user=user
        ).exclude(
            pattern__in=used_patterns
        ).order_by('mastery_score')

        for mastery in weak_patterns:
            if len(recommended) >= limit:
                break
            used_patterns.add(mastery.pattern)
            _add_problem_for_pattern(
                mastery,
                reason=f"Weak area: {mastery.pattern_display} ({mastery.mastery_score:.0f}% mastery)",
            )

    # 4. Fill with unseen patterns
    if len(recommended) < limit:
        practiced_patterns = set(
            PatternMastery.objects.filter(user=user).values_list('pattern', flat=True)
        )
        unseen_problems = Problem.objects.filter(
            is_active=True
        ).exclude(
            pattern__in=practiced_patterns
        ).exclude(
            id__in=solved_ids
        )

        for problem in unseen_problems:
            if len(recommended) >= limit:
                break
            recommended.append({
                'problem': problem,
                'reason': f'New pattern to try: {problem.get_pattern_display()}',
                'mastery': None,
            })

    return recommended
