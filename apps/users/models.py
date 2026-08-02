from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Custom user model with DSA learning profile fields."""

    LANGUAGE_CHOICES = [
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('go', 'Go'),
        ('rust', 'Rust'),
        ('typescript', 'TypeScript'),
        ('csharp', 'C#'),
    ]

    bio = models.TextField(max_length=500, blank=True, default='')
    preferred_language = models.CharField(
        max_length=20,
        choices=LANGUAGE_CHOICES,
        default='python'
    )
    leetcode_username = models.CharField(max_length=100, blank=True, default='', db_index=True)
    last_leetcode_sync = models.DateTimeField(null=True, blank=True)
    leetcode_total_solved = models.PositiveIntegerField(default=0)
    gfg_username = models.CharField(max_length=100, blank=True, default='', db_index=True)
    last_gfg_sync = models.DateTimeField(null=True, blank=True)
    gfg_total_solved = models.PositiveIntegerField(default=0)
    platform_stats_json = models.JSONField(default=dict, blank=True)
    streak = models.PositiveIntegerField(default=0)
    longest_streak = models.PositiveIntegerField(default=0)
    solved_count = models.PositiveIntegerField(default=0)
    xp = models.PositiveIntegerField(default=0)
    last_active_date = models.DateField(null=True, blank=True)
    avatar_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        ordering = ['-created_at']

    def __str__(self):
        return self.username

    def update_streak(self):
        """Update the user's daily streak."""
        from django.utils import timezone
        today = timezone.now().date()

        if self.last_active_date is None:
            self.streak = 1
        elif self.last_active_date == today:
            return  # Already active today
        elif (today - self.last_active_date).days == 1:
            self.streak += 1
        else:
            self.streak = 1

        self.last_active_date = today
        if self.streak > self.longest_streak:
            self.longest_streak = self.streak
        self.save(update_fields=['streak', 'longest_streak', 'last_active_date'])
