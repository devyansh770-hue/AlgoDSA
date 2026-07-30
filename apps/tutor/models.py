from django.db import models
from django.conf import settings


class ChatMessage(models.Model):
    """AI Tutor chat message."""

    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'AI Tutor'),
        ('system', 'System'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='chat_messages'
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    content = models.TextField()
    hint_level = models.PositiveSmallIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'chat_messages'
        ordering = ['created_at']

    def __str__(self):
        return f"{self.role}: {self.content[:50]}..."


class ExplanationAttempt(models.Model):
    """User's explanation of a solution (Explain It Back feature)."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='explanation_attempts'
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='explanation_attempts'
    )
    explanation = models.TextField()
    ai_feedback = models.TextField(blank=True, default='')
    is_approved = models.BooleanField(default=False)
    score = models.FloatField(default=0.0)  # 0-100
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'explanation_attempts'
        ordering = ['-created_at']

    def __str__(self):
        status = '✅' if self.is_approved else '❌'
        return f"{status} {self.user.username} - {self.problem.title}"
