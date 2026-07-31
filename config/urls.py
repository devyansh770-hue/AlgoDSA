"""
URL configuration for AlgoDSA project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from apps.users.views import landing_page

from apps.problems import views as problem_views
from apps.submissions import views as submission_views
from apps.progress import views as progress_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landing_page, name='landing'),
    path('auth/', include('apps.users.urls')),
    path('accounts/', include('allauth.urls')),
    path('learn/', problem_views.learn_hub_view, name='learn_hub'),
    path('learn/<slug:topic_slug>/', problem_views.learn_topic_view, name='learn_topic'),
    path('simulator/', problem_views.algorithm_simulator, name='algorithm_simulator'),
    path('interview/', problem_views.mock_interview, name='mock_interview'),
    path('mistakes/', submission_views.mistake_library, name='mistake_library'),
    path('career/', progress_views.career_readiness, name='career_readiness'),
    path('topics/', include('apps.problems.urls')),
    path('submissions/', include('apps.submissions.urls')),
    path('dashboard/', include('apps.progress.urls')),
    path('tutor/', include('apps.tutor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
