from django.contrib import admin
from .models import Submission


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'status', 'runtime_ms', 'memory_kb', 'created_at')
    list_filter = ('status', 'language', 'problem__topic')
    search_fields = ('user__username', 'problem__title')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)
