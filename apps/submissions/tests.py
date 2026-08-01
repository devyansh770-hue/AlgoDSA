from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User
from apps.problems.models import Topic, Problem, TestCase as ProblemTestCase
from apps.submissions.models import Submission, MistakeRecord


class SubmissionsTests(TestCase):
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
            pattern='two_pointers',
            starter_code_python='print("[0,1]")'
        )

        self.test_case = ProblemTestCase.objects.create(
            problem=self.problem,
            input_data='[2,7,11,15]\n9',
            expected_output='[0,1]',
            is_sample=True
        )

    def test_submit_code_success(self):
        url = reverse('submit_code')
        payload = {
            'problem_id': self.problem.id,
            'code': 'print("[0,1]")',
            'language': 'python'
        }
        response = self.client.post(
            url,
            data=payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['status'], 'accepted')
        self.assertEqual(data['test_cases_passed'], 1)

    def test_submission_history(self):
        Submission.objects.create(
            user=self.user,
            problem=self.problem,
            code='print("[0,1]")',
            language='python',
            status='accepted'
        )
        response = self.client.get(reverse('submission_history'))
        self.assertEqual(response.status_code, 200)

    def test_submission_detail(self):
        sub = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            code='print("[0,1]")',
            language='python',
            status='accepted'
        )
        response = self.client.get(reverse('submission_detail', kwargs={'submission_id': sub.id}))
        self.assertEqual(response.status_code, 200)

    def test_submission_api_detail(self):
        sub = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            code='print("[0,1]")',
            language='python',
            status='accepted'
        )
        url = reverse('get_submission_detail_api', kwargs={'submission_id': sub.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['id'], sub.id)

    def test_mistake_library_view(self):
        sub = Submission.objects.create(
            user=self.user,
            problem=self.problem,
            code='bad_code',
            language='python',
            status='wrong_answer'
        )
        MistakeRecord.objects.create(
            user=self.user,
            submission=sub,
            problem=self.problem,
            error_category='general_logic',
            ai_remediation='Check your logic'
        )
        response = self.client.get(reverse('mistake_library'))
        self.assertEqual(response.status_code, 200)
