from django.urls import path
from . import views

urlpatterns = [
    path('submit/', views.submit_code, name='submit_code'),
    path('history/', views.submission_history, name='submission_history'),
    path('mistakes/', views.mistake_library, name='mistake_library'),
    path('<int:submission_id>/', views.submission_detail, name='submission_detail'),
    path('api/problem/<int:problem_id>/', views.get_problem_submissions_api, name='get_problem_submissions_api'),
    path('api/detail/<int:submission_id>/', views.get_submission_detail_api, name='get_submission_detail_api'),
]
