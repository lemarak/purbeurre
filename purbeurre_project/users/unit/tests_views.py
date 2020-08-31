from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from users.views import SignupPageView, UpdateUserPageView


class SignupPageTests(TestCase):

    def test_signup_view(self):
        """ test route """
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignupPageView.as_view().__name__
        )
