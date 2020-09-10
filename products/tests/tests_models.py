from django.test import TestCase
from django.contrib.auth import get_user_model

from products.models import Product, Category


class BaseModelTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        """Method called to prepare the test fixture."""
        super(BaseModelTestCase, cls).setUpClass()

        cls.category = Category(
            id_category="1à",
            name="category_test",
            products=1,
            visible=True
        )
        cls.category.save()

        cls.product = Product(
            id_product="1é",
            product_name_fr='test',
            nutriscore_score=0,
            nutriscore_grade='A'
        )
        cls.product.save()
        cls.product.categories.add(cls.category)

        cls.User = get_user_model()
        cls.user = cls.User.objects.create(
            username='test',
            email='test@example.com',
            password='123test'
        )
        cls.product.favorites.add(cls.user)


class CategoryModelTestCase(BaseModelTestCase):
    """Class to test the creation of categories."""
    def test_create_category(self):
        """test creation."""
        max_length = self.category._meta.get_field('name').max_length
        self.assertEqual(self.category.name, 'category_test')
        self.assertEqual(max_length, 255)

    def test_object_category_name_is_name(self):
        """test field name is correct."""
        self.assertEqual(str(self.category), self.category.name)


class ProductModelTestCase(BaseModelTestCase):
    """Class for testing product management."""
    def test_create_product(self):
        """test the creation of products."""
        max_length = self.product._meta.get_field('product_name_fr').max_length
        self.assertEqual(self.product.product_name_fr, 'test')
        self.assertEqual(self.product.slug, '1e')
        self.assertEqual(max_length, 255)

    def test_product_category(self):
        """Tests the association of a product to a category."""
        self.assertEqual(True, self.category in self.product.categories.all())

    def test_absolute_url(self):
        """test the creation of url."""
        self.assertEqual(self.product.get_absolute_url(),
                         '/products/%s' % self.product.slug
                         )

    def test_object_product_name_is_product_name_fr(self):
        """test name of a product after creation."""
        self.assertEqual(str(self.product), self.product.product_name_fr)


class FavoriteModelTestCase(BaseModelTestCase):
    """test favourites."""
    def test_product_favorite_for_user(self):
        """Test adding a favorite for a user."""
        self.product.favorites.add(self.user)
        self.assertEqual(True, self.user in self.product.favorites.all())
