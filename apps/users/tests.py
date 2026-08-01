from django.test import TestCase, Client
from django.urls import reverse
from apps.users.models import User


class UserModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='Password123!',
            preferred_language='python'
        )

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.xp, 0)
        self.assertEqual(self.user.streak, 0)

    def test_update_streak(self):
        self.user.update_streak()
        self.assertEqual(self.user.streak, 1)
        self.assertEqual(self.user.longest_streak, 1)


class UserViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='Password123!'
        )

    def test_landing_page(self):
        response = self.client.get(reverse('landing'))
        self.assertEqual(response.status_code, 200)

    def test_register_view(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

        post_data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'Password123!',
            'password2': 'Password123!',
            'preferred_language': 'python',
        }
        response = self.client.post(reverse('register'), post_data)
        self.assertEqual(response.status_code, 302)  # Redirects to dashboard
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login_logout(self):
        login_success = self.client.login(username='testuser', password='Password123!')
        self.assertTrue(login_success)

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
