from django.db import models
from django.conf import settings


class Submission(models.Model):
    """A code submission for a problem."""

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('running', 'Running'),
        ('accepted', 'Accepted'),
        ('wrong_answer', 'Wrong Answer'),
        ('time_limit', 'Time Limit Exceeded'),
        ('memory_limit', 'Memory Limit Exceeded'),
        ('runtime_error', 'Runtime Error'),
        ('compilation_error', 'Compilation Error'),
    ]

    LANGUAGE_CHOICES = [
        ('python', 'Python'),
        ('javascript', 'JavaScript'),
        ('cpp', 'C++'),
        ('java', 'Java'),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    problem = models.ForeignKey(
        'problems.Problem',
        on_delete=models.CASCADE,
        related_name='submissions'
    )
    code = models.TextField()
    language = models.CharField(max_length=20, choices=LANGUAGE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    runtime_ms = models.FloatField(null=True, blank=True)
    memory_kb = models.FloatField(null=True, blank=True)
    test_cases_passed = models.PositiveIntegerField(default=0)
    test_cases_total = models.PositiveIntegerField(default=0)
    stdout = models.TextField(blank=True, default='')
    stderr = models.TextField(blank=True, default='')
    failure_reason = models.TextField(blank=True, default='')
    ai_review = models.TextField(blank=True, default='')
    judge0_token = models.CharField(max_length=100, blank=True, default='')
    is_leetcode_synced = models.BooleanField(default=False, db_index=True)
    leetcode_submission_id = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'submissions'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user.username} - {self.problem.title} - {self.get_status_display()}"

    @property
    def status_color(self):
        colors = {
            'accepted': '#10b981',
            'wrong_answer': '#ef4444',
            'time_limit': '#f59e0b',
            'memory_limit': '#f59e0b',
            'runtime_error': '#ef4444',
            'compilation_error': '#ef4444',
            'pending': '#6366f1',
            'running': '#06b6d4',
        }
        return colors.get(self.status, '#94a3b8')

    @property
    def status_icon(self):
        icons = {
            'accepted': '✅',
            'wrong_answer': '❌',
            'time_limit': '⏰',
            'memory_limit': '💾',
            'runtime_error': '💥',
            'compilation_error': '🔧',
            'pending': '⏳',
            'running': '🔄',
        }
        return icons.get(self.status, '❓')
