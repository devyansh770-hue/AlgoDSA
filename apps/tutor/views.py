import json
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import ChatMessage, ExplanationAttempt
from apps.problems.models import Problem
from .services.ai import AIService


@login_required
@require_POST
def get_ai_hint(request):
    """Get an AI hint for a problem at the specified level."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    level = data.get('level', 1)
    user_code = data.get('code', '')

    if not problem_id:
        return JsonResponse({'error': 'Problem ID required'}, status=400)

    if level not in [1, 2, 3]:
        return JsonResponse({'error': 'Level must be 1, 2, or 3'}, status=400)

    problem = get_object_or_404(Problem, id=problem_id)

    # First, try to use stored hints
    from apps.problems.models import Hint
    stored_hint = Hint.objects.filter(problem=problem, level=level).first()

    if stored_hint:
        hint_text = stored_hint.content
    else:
        # Fall back to AI-generated hint
        ai = AIService()
        hint_text = ai.get_hint(problem, level, user_code)

    # Save chat message
    ChatMessage.objects.create(
        user=request.user,
        problem=problem,
        role='user',
        content=f'Requested Level {level} hint',
        hint_level=level,
    )
    ChatMessage.objects.create(
        user=request.user,
        problem=problem,
        role='assistant',
        content=hint_text,
        hint_level=level,
    )

    return JsonResponse({
        'hint': hint_text,
        'level': level,
    })


@login_required
@require_POST
def submit_explanation(request):
    """Submit an explanation for the 'Explain It Back' feature."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    explanation = data.get('explanation', '')

    if not problem_id or not explanation.strip():
        return JsonResponse({'error': 'Problem ID and explanation required'}, status=400)

    problem = get_object_or_404(Problem, id=problem_id)

    # Check with AI
    ai = AIService()
    result = ai.check_explanation(problem, explanation)

    # Save attempt
    attempt = ExplanationAttempt.objects.create(
        user=request.user,
        problem=problem,
        explanation=explanation,
        ai_feedback=result['feedback'],
        is_approved=result['approved'],
        score=result['score'],
    )

    return JsonResponse({
        'approved': result['approved'],
        'score': result['score'],
        'feedback': result['feedback'],
        'editorial': problem.editorial if result['approved'] else None,
    })


@login_required
def get_chat_history(request, problem_id):
    """Get chat history for a problem."""
    problem = get_object_or_404(Problem, id=problem_id)
    messages = ChatMessage.objects.filter(
        user=request.user,
        problem=problem
    ).order_by('created_at')

    data = [{
        'role': msg.role,
        'content': msg.content,
        'hint_level': msg.hint_level,
        'created_at': msg.created_at.isoformat(),
    } for msg in messages]

    return JsonResponse({'messages': data})


@login_required
@require_POST
def validate_approach(request):
    """Pre-code approach check API (Feature 1)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    approach_type = data.get('approach_type', 'brute_force')
    explanation = data.get('explanation', '')

    problem = get_object_or_404(Problem, id=problem_id)
    ai = AIService()
    res = ai.validate_approach(problem, approach_type, explanation)
    return JsonResponse(res)


@login_required
@require_POST
def get_socratic_debug(request):
    """Socratic debugging hints for failed runs (Feature 2)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    code = data.get('code', '')
    error_log = data.get('error_log', '')

    problem = get_object_or_404(Problem, id=problem_id)
    ai = AIService()
    res = ai.get_socratic_debug_hint(problem, code, error_log)
    return JsonResponse(res)


@login_required
@require_POST
def get_post_solve_review(request):
    """Comprehensive AI code review post-Accepted (Feature 3)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    code = data.get('code', '')
    runtime_ms = data.get('runtime_ms')
    memory_kb = data.get('memory_kb')

    problem = get_object_or_404(Problem, id=problem_id)
    ai = AIService()
    res = ai.generate_comprehensive_review(problem, code, runtime_ms, memory_kb)
    return JsonResponse(res)


@login_required
@require_POST
def post_solve_reflection(request):
    """SM-2 post-solve reflection rating update (Feature 5)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    rating = data.get('rating', 'easy')  # 'easy', 'medium', 'hard'

    problem = get_object_or_404(Problem, id=problem_id)
    from apps.progress.services.spaced_repetition import record_review
    quality_map = {'easy': 5, 'medium': 3, 'hard': 1}
    quality = quality_map.get(rating, 4)
    record_review(request.user, problem, quality)

    return JsonResponse({'status': 'ok', 'rating': rating, 'message': 'SM-2 schedule updated successfully!'})


@login_required
@require_POST
def teach_ai(request):
    """Teach the AI explanation evaluation (Feature 6)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    problem_id = data.get('problem_id')
    explanation = data.get('explanation', '')

    problem = get_object_or_404(Problem, id=problem_id)
    ai = AIService()
    res = ai.evaluate_teaching_explanation(problem, explanation)
    
    if res['approved']:
        request.user.xp += res['xp_awarded']
        request.user.save()

    res['user_xp'] = request.user.xp
    return JsonResponse(res)


@login_required
@require_POST
def submit_micro_drill(request):
    """Daily 30-Second Micro Drill submission (Feature 7)."""
    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON'}, status=400)

    selected_option = data.get('option')
    is_correct = selected_option == 'correct'

    if is_correct:
        request.user.xp += 15
        request.user.save()

    return JsonResponse({
        'is_correct': is_correct,
        'xp_gained': 15 if is_correct else 0,
        'user_xp': request.user.xp,
        'message': '🎉 Correct! +15 XP awarded.' if is_correct else 'Not quite, but great effort! Keep practicing.'
    })
