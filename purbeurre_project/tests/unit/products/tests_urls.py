from django.test import TestCase
from django.urls import reverse


class ProductsUrlTests(TestCase):

    def test_detail_url(self):
        """ test the detail product url """
        url = reverse('product_detail', args=[1234])
        self.assertEqual(url, '/products/1234')

    def test_search_url(self):
        """ test the search products url """
        url = url = "%s?search=test" % reverse('search')
        self.assertEqual(url, '/products/search/?search=test')

    def test_substitutes_for_product_url(self):
        """ test the substitutes for a product url """
        url = url = reverse('substitutes', args=[1234])
        self.assertEqual(url, '/products/substitutes/1234')

    def test_favorites_for_user_url(self):
        """ test the favorites for a user url """
        url = url = reverse('favorites')
        self.assertEqual(url, '/products/substitutes/favorites/')

    def test_add_favorites_url(self):
        """ test the url for adding a favorite product """
        url = url = reverse('admin_favorite', args=[1234, "add"])
        self.assertEqual(url, '/products/favorite/1234/add/')

    def test_del_favorites_url(self):
        """ test the url for deleting a favorite product """
        url = url = reverse('admin_favorite', args=[1234, "del"])
        self.assertEqual(url, '/products/favorite/1234/del/')
