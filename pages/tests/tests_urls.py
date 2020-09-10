"""test urls's pages."""
from django.test import SimpleTestCase
from django.urls import reverse


class PagesUrlTests(SimpleTestCase):
    """each method test url given by urls.py."""

    def test_home_url(self):
        """test the home url."""
        url = reverse('home')
        self.assertEqual(url, '/')

    def test_legal_url(self):
        """test the legals notices url."""
        url = reverse('legal')
        self.assertEqual(url, '/legal/')
