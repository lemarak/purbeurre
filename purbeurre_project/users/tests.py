from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse, resolve

from .views import SignupPageView, UpdateUserPageView


class CustomUserTests(TestCase):
    """ tests users application """

    def setUp(self):
        self.User = get_user_model()

    def test_create_user(self):
        """ Tests the creation of a user """

        user = self.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test',
            name='TestName',  # Field created for the application
            bio='Ma biographie'  # Field created for the application
        )
        self.assertEqual(user.username, 'test')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.name, 'TestName')
        self.assertEqual(user.bio, 'Ma biographie')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """ Tests the creation of a super user """

        superUser = self.User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='123test',
        )
        self.assertEqual(superUser.username, 'admin')
        self.assertEqual(superUser.email, 'admin@example.com')
        self.assertTrue(superUser.is_active)
        self.assertTrue(superUser.is_superuser)

    # def test_duplicate_users(self):
    #     with self.assertRaises(TypeError) as foo:
    #         user1 = self.User.objects.create(
    #             username='test',
    #             email='test@example.com',
    #             password='123test',
    #         )
    #         user2 = self.User.objects.create(
    #             username='test',
    #             email='test@example.com',
    #             password='123test',
    #         )
    #     self.assertEqual("???", str(foo.exception), "???")


class SignupPageTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_page(self):
        """ test the signup page """
        self.assertContains(self.response, 'Inscription')
        self.assertEqual(self.response.status_code, 200)

    def test_signup_view(self):
        """ test route """
        view = resolve('/accounts/signup/')
        self.assertEqual(
            view.func.__name__,
            SignupPageView.as_view().__name__
        )
