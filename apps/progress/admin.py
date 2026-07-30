from django.contrib import admin
from .models import PatternMastery, TopicProgress


@admin.register(PatternMastery)
class PatternMasteryAdmin(admin.ModelAdmin):
    list_display = ('user', 'pattern', 'mastery_score', 'attempts', 'correct', 'next_review')
    list_filter = ('pattern',)
    search_fields = ('user__username',)


@admin.register(TopicProgress)
class TopicProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'topic', 'problems_attempted', 'problems_solved', 'last_practiced')
    list_filter = ('topic',)
    search_fields = ('user__username',)
