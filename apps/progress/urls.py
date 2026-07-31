from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('career/', views.career_readiness, name='career_readiness'),
    path('sync-leetcode/', views.sync_leetcode_view, name='sync_leetcode'),
    path('sync-gfg/', views.sync_gfg_view, name='sync_gfg'),
    path('sync-all/', views.sync_all_platforms_view, name='sync_all_platforms'),
]
