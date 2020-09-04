from unittest.mock import MagicMock, patch

from django.test import TestCase

from products.management.commands import import_api
from products.models import Product, Category


class ManageProductTest(TestCase):

    def setUp(self):
        self.command = import_api.Command()
        self.category_dict = {
            'id': 'id_test',
            'name': 'test_category',
            'products': 200,
            'url': 'http://mytesturl.com'
        }
        self.product_dict = {
            '_id': 'key1',
            'product_name_fr': 'test_name',
            'nutriscore_score': 0,
            'nutriscore_grade': 'A',
            'stores': 'magasin',
            'generic_name_fr': 'description',
            'brands': 'marque',
            'url': 'http://www.monurl.com',
            'nutriments': {
                "fat_100g": 2,
                "saturated-fat_100g": 2,
                "sugars_100g": 2,
                "salt_100g": 2,
            },
        }

    @patch('requests.get')
    def tests_request_api_categories(self, get):
        response = self.command.request_api_categories()
        self.assertTrue(get.called)

    def test_save_category(self):
        self.command.add_category(self.category_dict)
        self.assertEqual(Category.objects.count(), 1)

    @patch('requests.get')
    def tests_request_api_products(self, get):
        category = MagicMock()
        response = self.command.request_api_products(category)
        self.assertTrue(get.called)

    def test_save_product(self):
        self.command.add_category(self.category_dict)
        self.command.add_product(self.product_dict, self.category_dict['id'])
        self.assertEqual(Product.objects.count(), 1)

    def test_save_product_mandatory_missing(self):
        self.command.add_category(self.category_dict)
        product_ko = self.product_dict
        del product_ko['nutriscore_grade']
        self.command.add_product(product_ko, self.category_dict['id'])
        self.assertEqual(Product.objects.count(), 0)
