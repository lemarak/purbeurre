"""Test the View module for products."""
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

from products.models import Product, Category


class ProductsViewTest(TestCase):
    """Test the views of a product."""
    @classmethod
    def setUpTestData(cls):
        """Method called to prepare the test fixture."""
        cls.category = Category(
            id_category="1à",
            name="category_test",
            products=1,
            visible=True
        )
        cls.category.save()

        cls.User = get_user_model()
        cls.user = cls.User.objects.create_user(
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

        cls.client_login = Client(HTTP_REFERER=reverse('home'))
        cls.logged_in = cls.client_login.login(
            username='test@example.com', password='123test')

    def test_search_pagination_is_six(self):
        """check pagination by six for search."""
        url = "%s?search=test" % reverse('search')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['products']) == 6)

    def test_lists_all_products_from_search(self):
        """test if all products returned by search, second page called."""
        url = "%s?search=test" % reverse('search')
        response = self.client.get(url+'&page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['products']) == 5)

    def test_substitutes_pagination_is_six(self):
        """check pagination by six for substitutes."""
        url = reverse('substitutes', args=['key1'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['substitutes']) == 6)

    def test_lists_all_products_from_substitutes(self):
        """test if all substitutes returned for a product, second page
        called."""
        url = reverse('substitutes', args=['key1'])
        response = self.client.get(url+'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'])
        self.assertTrue(len(response.context['substitutes']) == 4)

    def test_favorites_pagination_is_six(self):
        """test favourite page."""
        url = reverse('favorites')
        response = self.client_login.get(url)
        self.assertTrue(self.logged_in)
        self.assertEqual(response.context['user'].email, 'test@example.com')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(len(response.context['favorites']) == 6)

    def test_add_favorite(self):
        """Test adding a favorite."""
        product_to_fav = Product(
            id_product="fav01",
            product_name_fr="test_favori",
            nutriscore_score=0,
            nutriscore_grade='A'
        )
        product_to_fav.save()
        url = reverse('admin_favorite',
                      args=['fav01', 'add'])
        response = self.client_login.get(url)
        user = self.User.objects.get(username='test')
        favorites = Product.objects.filter(favorites=user)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(favorites), 12)
        self.assertTrue(product_to_fav in user.product_set.all())

    def test_del_favorite(self):
        """Test deleting a favorite."""
        url = reverse('admin_favorite',
                      args=['key0', 'del'])
        response = self.client_login.get(url)
        favorites = Product.objects.filter(favorites=self.user)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(len(favorites), 10)
        self.assertTrue(Product.objects.get(pk='key0')
                        not in self.user.product_set.all())

    def test_page_detail(self):
        """Test the detail page of a product."""
        url = reverse('product_detail', args=['key1'])
        response = self.client_login.get(url)
        html = response.content.decode('utf8')
        self.assertEqual(response.status_code, 200)
        self.assertInHTML("""
          <h3 class="text-white">test_1 (category_test)</h3>
        """, html)
