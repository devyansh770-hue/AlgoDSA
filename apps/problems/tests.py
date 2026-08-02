from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.problems.models import Topic, Problem, TestCase as ProblemTestCase, Hint, Pattern


class ProblemViewsTests(TestCase):
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
            description='Array data structure',
            icon='📚',
            color='#6366f1',
            order=1
        )

        self.problem = Problem.objects.create(
            topic=self.topic,
            title='Two Sum',
            slug='two-sum',
            description='Find two numbers that add up to target.',
            difficulty='easy',
            pattern='two_pointers',
            starter_code_python='def twoSum(nums, target):\n    pass',
            starter_code_javascript='function twoSum(nums, target) {}',
            is_active=True
        )

        self.test_case = ProblemTestCase.objects.create(
            problem=self.problem,
            input_data='[2,7,11,15]\n9',
            expected_output='[0,1]',
            is_sample=True
        )

        self.hint = Hint.objects.create(
            problem=self.problem,
            level=1,
            content='Use a hash map to store complements.'
        )

        self.pattern = Pattern.objects.create(
            topic=self.topic,
            name='Two Pointers',
            slug='two-pointers',
            description='Two pointers approach'
        )

    def test_topic_list_view(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse('topic_list'))
        self.assertEqual(response.status_code, 200)

    def test_problem_list_view(self):
        response = self.client.get(reverse('problem_list', kwargs={'topic_slug': 'arrays'}))
        self.assertEqual(response.status_code, 200)

    def test_problem_detail_view(self):
        response = self.client.get(reverse('problem_detail', kwargs={
            'topic_slug': 'arrays',
            'problem_slug': 'two-sum'
        }))
        self.assertEqual(response.status_code, 200)

    def test_learn_hub_view(self):
        response = self.client.get(reverse('learn_hub'))
        self.assertEqual(response.status_code, 200)

    def test_learn_topic_view(self):
        response = self.client.get(reverse('learn_topic', kwargs={'topic_slug': 'arrays'}))
        self.assertEqual(response.status_code, 200)

    def test_learn_pattern_view(self):
        response = self.client.get(reverse('learn_pattern', kwargs={
            'topic_slug': 'arrays',
            'pattern_slug': 'two-pointers'
        }))
        self.assertEqual(response.status_code, 200)

    def test_algorithm_simulator(self):
        response = self.client.get(reverse('algorithm_simulator'))
        self.assertEqual(response.status_code, 200)

    def test_mock_interview(self):
        response = self.client.get(reverse('mock_interview'))
        self.assertEqual(response.status_code, 200)

    def test_get_starter_code_api(self):
        url = reverse('get_starter_code', kwargs={'problem_id': self.problem.id})
        response = self.client.get(url + '?language=python')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('def twoSum', data['code'])
