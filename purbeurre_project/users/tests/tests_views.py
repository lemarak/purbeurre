"""Test the View module for users."""
from django.test import TestCase, Client
from django.contrib.auth import get_user_model, get_user
from django.urls import resolve

from users.views import SignupPageView


class SetUp(TestCase):
    """prepare the test fixture."""
    @classmethod
    def setUpTestData(cls):
        """Method called to prepare the test fixture."""
        cls.User = get_user_model()
        cls.user_test = cls.User.objects.create_user(
            username='test',
            email='test@example.com',
            password='123test'
        )


class SignupPageTests(TestCase):

    def test_signup_view(self):
        """test route."""
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignupPageView.as_view().__name__
        )


class SigninPageTests(SetUp):
    """test signin view."""

    def test_signin_page_view(self):
        """test signin page."""
        c = Client()
        response = c.post('/accounts/login/', {
            'username': 'test@example.com',
            'password': '123test'}
        )
        user = get_user(response.wsgi_request)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(user.is_authenticated)
        self.assertTrue(user.username, "test")
        self.assertTrue(user.email, "test@example.com")

    def test_login_view(self):
        """test login page."""
        c = Client()
        logged_in = c.login(email='test@example.com', password='123test')
        self.assertTrue(logged_in)
