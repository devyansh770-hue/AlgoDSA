from django.urls import path
from django.contrib.auth.views import LoginView
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', LoginView.as_view(
        template_name='registration/login.html',
        redirect_authenticated_user=True,
    ), name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
]
