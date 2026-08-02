from django.urls import path
from . import views

urlpatterns = [
    # Primary Topics & Learning Hub Routes
    path('', views.learn_hub_view, name='topic_list'),
    path('learn/', views.learn_hub_view, name='learn_hub'),

    # APIs
    path('api/search/', views.global_search_api, name='global_search_api'),
    path('api/sm2/record/', views.record_sm2_review, name='record_sm2_review'),
    path('api/hint/<int:problem_id>/<int:level>/', views.get_hint, name='get_hint'),
    path('api/starter-code/<int:problem_id>/', views.get_starter_code, name='get_starter_code'),

    # University Learn, Pattern & Lesson Routes
    path('learn/<slug:topic_slug>/', views.learn_topic_view, name='learn_topic'),
    path('learn/<slug:topic_slug>/<slug:pattern_slug>/', views.learn_pattern_view, name='learn_pattern'),
    path('learn/<slug:topic_slug>/<slug:pattern_slug>/<slug:lesson_slug>/', views.learn_lesson_view, name='learn_lesson'),

    # Legacy /topics/ Alias Routes
    path('topics/', views.learn_hub_view, name='topics_hub'),
    path('topics/<slug:topic_slug>/', views.learn_topic_view, name='topic_course_legacy'),
    path('topics/<slug:topic_slug>/<slug:pattern_slug>/', views.learn_pattern_view, name='learn_pattern_legacy'),
    path('topics/<slug:topic_slug>/<slug:pattern_slug>/<slug:lesson_slug>/', views.learn_lesson_view, name='learn_lesson_legacy'),

    # Problem List & Problem Detail Routes
    path('<slug:topic_slug>/', views.problem_list, name='problem_list'),
    path('<slug:topic_slug>/<slug:problem_slug>/', views.problem_detail, name='problem_detail'),
]
