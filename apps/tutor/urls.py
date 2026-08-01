from django.urls import path
from . import views

urlpatterns = [
    path('hint/', views.get_ai_hint, name='get_ai_hint'),
    path('explain/', views.submit_explanation, name='submit_explanation'),
    path('chat/<int:problem_id>/', views.get_chat_history, name='chat_history'),
    path('api/validate-approach/', views.validate_approach, name='validate_approach'),
    path('api/socratic-debug/', views.get_socratic_debug, name='socratic_debug'),
    path('api/post-solve-review/', views.get_post_solve_review, name='post_solve_review'),
    path('api/post-solve-reflection/', views.post_solve_reflection, name='post_solve_reflection'),
    path('api/teach-ai/', views.teach_ai, name='teach_ai'),
    path('api/micro-drill/', views.submit_micro_drill, name='submit_micro_drill'),
]
