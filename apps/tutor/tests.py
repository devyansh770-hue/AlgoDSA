from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.problems.models import Topic, Problem


class TutorTests(TestCase):
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

    def test_get_ai_hint(self):
        url = reverse('get_ai_hint')
        payload = {
            'problem_id': self.problem.id,
            'level': 1,
            'code': 'def twoSum(): pass'
        }
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('hint', data)

    def test_submit_explanation(self):
        url = reverse('submit_explanation')
        payload = {
            'problem_id': self.problem.id,
            'explanation': 'This problem can be solved using two_pointers. Time complexity is O(N).'
        }
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['approved'])

    def test_validate_approach(self):
        url = reverse('validate_approach')
        payload = {
            'problem_id': self.problem.id,
            'approach_type': 'two_pointers',
            'explanation': 'Using two pointers'
        }
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_teach_ai_awards_xp(self):
        url = reverse('teach_ai')
        payload = {
            'problem_id': self.problem.id,
            'explanation': 'First initialize left and right pointers at bounds, then shrink.'
        }
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, 15)

    def test_submit_micro_drill_awards_xp(self):
        url = reverse('submit_micro_drill')
        payload = {
            'option': 'correct'
        }
        response = self.client.post(url, data=payload, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.user.refresh_from_db()
        self.assertEqual(self.user.xp, 15)
