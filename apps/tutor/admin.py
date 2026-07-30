from django.contrib import admin
from .models import ChatMessage, ExplanationAttempt


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'role', 'hint_level', 'created_at')
    list_filter = ('role', 'hint_level')
    search_fields = ('user__username', 'content')


@admin.register(ExplanationAttempt)
class ExplanationAttemptAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'is_approved', 'score', 'created_at')
    list_filter = ('is_approved',)
    search_fields = ('user__username', 'explanation')
