from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Product, Category


class ProductsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.category = Category(
            id_category="1à",
            name="category_test",
            products=1,
            visible=True
        )
        cls.category.save()

        cls.User = get_user_model()
        cls.user = cls.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test'
        )

        nb_products = 11

        for id_product in range(nb_products):
            cls.product = Product(
                id_product="key%s" % id_product,
                product_name_fr="test_%s" % id_product,
                nutriscore_score=0,
                nutriscore_grade='A'
            )
            cls.product.save()
            cls.product.categories.add(cls.category)
            cls.product.favorites.add(cls.user)

    def test_search_pagination_is_six(self):
        url = "%s?search=test" % reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['products']) == 6)

    def test_lists_all_products_from_search(self):
        url = "%s?search=test" % reverse('search')
        response = self.client.get(url+'&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['products']) == 5)

    def test_substitutes_pagination_is_six(self):
        url = reverse('substitutes', args=['key1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['substitutes']) == 6)

    def test_lists_all_products_from_substitutes(self):
        url = reverse('substitutes', args=['key1'])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['substitutes']) == 4)

    def test_favorites_pagination_is_six(self):
        login = self.client.login(email='test@example.com', password='123test')
        url = reverse('favorites')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['favorites']) == 6)