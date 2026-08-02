from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('simulator/', views.algorithm_simulator, name='algorithm_simulator'),
    path('interview/', views.mock_interview, name='mock_interview'),
    path('learn/', views.learn_hub_view, name='learn_hub'),
    path('learn/<slug:topic_slug>/', views.learn_topic_view, name='learn_topic'),
    path('learn/<slug:topic_slug>/<slug:pattern_slug>/', views.learn_pattern_view, name='learn_pattern'),
    path('learn/<slug:topic_slug>/<slug:pattern_slug>/<slug:lesson_slug>/', views.learn_lesson_view, name='learn_lesson'),
    path('topics/<slug:topic_slug>/', views.learn_topic_view, name='topic_course_legacy'),
    path('api/search/', views.global_search_api, name='global_search_api'),
    path('api/sm2/record/', views.record_sm2_review, name='record_sm2_review'),
    path('<slug:topic_slug>/', views.problem_list, name='problem_list'),
    path('<slug:topic_slug>/<slug:problem_slug>/', views.problem_detail, name='problem_detail'),
    path('api/hint/<int:problem_id>/<int:level>/', views.get_hint, name='get_hint'),
    path('api/starter-code/<int:problem_id>/', views.get_starter_code, name='get_starter_code'),
]
