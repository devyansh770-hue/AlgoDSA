from django.db import models
from django.conf import settings


class PatternMastery(models.Model):
    """Tracks user mastery of each DSA pattern."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='pattern_masteries'
    )
    pattern = models.CharField(max_length=30)  # Matches Problem.PATTERN_CHOICES
    attempts = models.PositiveIntegerField(default=0)
    correct = models.PositiveIntegerField(default=0)
    mastery_score = models.FloatField(default=0.0)  # 0-100
    # Spaced repetition fields (SM-2 algorithm)
    ease_factor = models.FloatField(default=2.5)
    interval_days = models.PositiveIntegerField(default=1)
    repetitions = models.PositiveIntegerField(default=0)
    next_review = models.DateField(null=True, blank=True)
    last_reviewed = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'pattern_mastery'
        unique_together = ['user', 'pattern']
        ordering = ['-mastery_score']

    def __str__(self):
        return f"{self.user.username} - {self.pattern}: {self.mastery_score}%"

    @property
    def pattern_display(self):
        """Human-readable pattern name."""
        from apps.problems.models import Problem
        pattern_dict = dict(Problem.PATTERN_CHOICES)
        return pattern_dict.get(self.pattern, self.pattern)

    @property
    def mastery_color(self):
        if self.mastery_score >= 80:
            return '#10b981'  # Green
        elif self.mastery_score >= 50:
            return '#f59e0b'  # Amber
        elif self.mastery_score >= 25:
            return '#f97316'  # Orange
        return '#ef4444'  # Red


class TopicProgress(models.Model):
    """Tracks user progress within each topic."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='topic_progresses'
    )
    topic = models.ForeignKey(
        'problems.Topic',
        on_delete=models.CASCADE,
        related_name='progresses'
    )
    problems_attempted = models.PositiveIntegerField(default=0)
    problems_solved = models.PositiveIntegerField(default=0)
    last_practiced = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = 'topic_progress'
        unique_together = ['user', 'topic']

    def __str__(self):
        return f"{self.user.username} - {self.topic.name}: {self.problems_solved}/{self.problems_attempted}"

    @property
    def progress_percentage(self):
        total = self.topic.problems.filter(is_active=True).count()
        if total == 0:
            return 0
        return int(self.problems_solved / total * 100)
