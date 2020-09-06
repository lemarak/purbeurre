import time

from django.test import LiveServerTestCase
from django.contrib.auth import get_user_model

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys

from products.models import Product, Category


class ProductsChrome(LiveServerTestCase):
    """functional tests using selenium and TestCase."""
    def setUp(self):
        """Method called to prepare the test fixture."""
        self.browser = Chrome()
        self.options = ChromeOptions()
        self.options.add_experimental_option("excludeSwitches",
                                             ["enable-logging"])
        User = get_user_model()
        self.user = User.objects.create_user(
            username='test',
            email='test@example.com',
            password='123test'
        )

        self.category = Category(
            id_category="1à",
            name="category_test",
            products=1,
            visible=True
        )
        self.category.save()

        for id_product in range(7):
            self.product = Product(
                id_product="key%s" % id_product,
                product_name_fr="test_%s" % id_product,
                nutriscore_score=0,
                nutriscore_grade='A',
                brands='brand_test'
            )
            self.product.save()
            self.product.categories.add(self.category)

    def tearDown(self):
        """Method called immediately after the test method has been called and
        the result recorded."""
        self.browser.quit()

    def login_user(self, email, pwd):
        """method simulating the connection of a user."""
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/login/'))
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys(email)
        password_input.send_keys(pwd)
        submission_button.click()

    def search_product(self, action_id):
        """ method simulating the search for a product
        param: action_id (search-form or search-nav) """
        self.browser.get(str(self.live_server_url))
        # search
        search_input = self.browser.find_element_by_id(action_id)
        submission_button = self.browser.find_element_by_class_name(
            'btn-primary')
        search_input.send_keys('test_')
        if (action_id == 'search-form'):
            submission_button.click()
        else:
            search_input.send_keys(Keys.ENTER)
        time.sleep(2)

    def test_search_product_with_form(self):
        """test search from form."""
        self.search_product('search-form')
        html = self.browser.page_source
        self.assertInHTML("""
        <h4 class="text-white">Votre recherche a renvoyé <strong>7</strong>
                produits correspondant à <strong>test_ </strong></h4>""",
                          html)

    def test_search_product_with_nav(self):
        """test the search from the nav bar."""
        self.search_product('search-nav')
        html = self.browser.page_source
        self.assertInHTML("""
        <h4 class="text-white">Votre recherche a renvoyé <strong>7</strong>
                produits correspondant à <strong>test_ </strong></h4>""",
                          html)

    def test_search_product_and_page_next(self):
        """test next page with search."""
        self.browser.get(
            "%s%s" %
            (str(self.live_server_url),
             '/products/search/?search=test'))
        html = self.browser.page_source

        # next page
        next_button = self.browser.find_element_by_class_name(
            'page-link')
        next_button.click()
        time.sleep(2)
        html = self.browser.page_source
        current_url = self.browser.current_url
        expected_url = "%s%s" % (
            str(self.live_server_url),
            '/products/search/?search=test&page=2')
        self.assertEqual(expected_url,
                         current_url)
        self.assertInHTML("""
                    <p class="text-white bg-primary p-2">
                            Page 2 of 2.
                        </p>
                        """,
                          html)

    def test_get_substitutes(self):
        """test substitutes page."""
        self.browser.get(
            "%s%s" %
            (str(self.live_server_url),
             '/products/search/?search=test'))
        a_button = self.browser.find_element_by_id('link-key1')
        a_button.click()
        time.sleep(1)
        html = self.browser.page_source
        current_url = self.browser.current_url
        expected_url = "%s%s" % (
            str(self.live_server_url),
            '/products/substitutes/key1')
        self.assertEqual(expected_url,
                         current_url)
        self.assertInHTML("""
                    <h4 class="text-white">Vous pouvez remplacer <strong>test_1
                    (brand_test)</strong></h4>
                        """,
                          html)

    def test_add_fav(self):
        """test adding favorites."""
        self.login_user('test@example.com', '123test')
        self.browser.get(
            "%s%s" %
            (str(self.live_server_url),
             '/products/key1'))
        time.sleep(1)
        fav_button = self.browser.find_element_by_id('add-fav')
        fav_button.click()
        time.sleep(1)
        html = self.browser.page_source
        self.assertInHTML("""
            Retirer
                """,
                          html)
