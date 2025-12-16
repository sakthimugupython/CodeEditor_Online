from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import CodeSnippet, ExecutionHistory, UserProfile

class UserAuthenticationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
    
    def test_user_registration(self):
        response = self.client.post('/accounts/register/', {
            'username': 'newuser',
            'email': 'new@example.com',
            'password1': 'securepass123',
            'password2': 'securepass123',
        })
        self.assertEqual(User.objects.filter(username='newuser').count(), 1)
    
    def test_user_login(self):
        response = self.client.post('/accounts/login/', {
            'username': 'testuser',
            'password': 'testpass123',
        })
        self.assertEqual(response.status_code, 302)
    
    def test_user_profile_creation(self):
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

class CodeSnippetTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
        self.client = Client()
        self.client.login(username='testuser', password='testpass123')
    
    def test_create_snippet(self):
        snippet = CodeSnippet.objects.create(
            user=self.user,
            title='Test Snippet',
            code='print("Hello")',
            language='python'
        )
        self.assertEqual(snippet.title, 'Test Snippet')
        self.assertEqual(snippet.language, 'python')
    
    def test_snippet_count_update(self):
        initial_count = self.user.profile.total_snippets
        CodeSnippet.objects.create(
            user=self.user,
            title='Test',
            code='print("test")',
            language='python'
        )
        self.user.profile.refresh_from_db()
        self.assertEqual(self.user.profile.total_snippets, initial_count + 1)

class ExecutionHistoryTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('testuser', 'test@example.com', 'testpass123')
    
    def test_create_execution(self):
        execution = ExecutionHistory.objects.create(
            user=self.user,
            code='print("test")',
            language='python',
            stdout='test\n',
            status='success'
        )
        self.assertEqual(execution.status, 'success')
        self.assertEqual(execution.language, 'python')
