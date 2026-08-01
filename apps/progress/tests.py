from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.problems.models import Topic, Problem
from apps.progress.models import TopicProgress, PatternMastery


class ProgressTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='Password123!'
        )
        self.client.force_login(self.user)

        self.topic = Topic.objects.create(
            name='Arrays',
            slug='arrays',
            order=1
        )

        self.problem = Problem.objects.create(
            topic=self.topic,
            title='Two Sum',
            slug='two-sum',
            description='Two Sum problem',
            difficulty='easy',
            pattern='two_pointers'
        )

        self.tp = TopicProgress.objects.create(
            user=self.user,
            topic=self.topic,
            problems_attempted=1,
            problems_solved=1
        )

        self.pm = PatternMastery.objects.create(
            user=self.user,
            pattern='two_pointers',
            attempts=1,
            correct=1,
            mastery_score=100.0
        )

    def test_dashboard_view(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('topic_progresses', response.context)

    def test_career_readiness_view(self):
        response = self.client.get(reverse('career_readiness'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('company_readiness', response.context)
