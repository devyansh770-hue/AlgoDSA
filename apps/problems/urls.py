from django.urls import path
from . import views

urlpatterns = [
    path('', views.topic_list, name='topic_list'),
    path('learn/', views.learn_hub_view, name='learn_hub'),
    path('learn/<slug:topic_slug>/', views.learn_topic_view, name='learn_topic'),
    path('learn/<slug:topic_slug>/<slug:pattern_slug>/', views.learn_pattern_view, name='learn_pattern'),
    path('<slug:topic_slug>/', views.problem_list, name='problem_list'),
    path('<slug:topic_slug>/<slug:problem_slug>/', views.problem_detail, name='problem_detail'),
    path('api/hint/<int:problem_id>/<int:level>/', views.get_hint, name='get_hint'),
    path('api/starter-code/<int:problem_id>/', views.get_starter_code, name='get_starter_code'),
]
