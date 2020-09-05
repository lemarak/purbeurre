import time

from django.test import LiveServerTestCase

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from django.contrib.auth import get_user_model


class SignUpTest(LiveServerTestCase):

    def setUp(self):
        self.browser = Chrome()

    def tearDown(self):
        self.browser.quit()

    def signup_form(self, action):
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/signup/'))
        email_input = self.browser.find_element_by_id('id_email')
        username_input = self.browser.find_element_by_id('id_username')
        password1_input = self.browser.find_element_by_id('id_password1')
        password2_input = self.browser.find_element_by_id('id_password2')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys('test_username_selenium')
        email_input.send_keys('test_email_selenium@example.com')
        password1_input.send_keys('test_1234')
        password2_input.send_keys('test_1234')
        if (action == "button"):
            submission_button.click()
        else:
            password2_input.send_keys(Keys.ENTER)
        time.sleep(0.5)
        redirection_url = str(self.live_server_url) + "/accounts/login/"
        current_url = self.browser.current_url
        self.assertEqual(redirection_url,
                         current_url)

    def test_signup_with_button(self):
        self.signup_form('button')

    def test_signup_with_key(self):
        self.signup_form('key')


class SignInFormTest(LiveServerTestCase):

    def setUp(self):
        self.browser = Chrome()
        User = get_user_model()
        User.objects.create_user(
            username='test_login',
            email='test_login@example.com',
            password='123test'
        )

    def tearDown(self):
        self.browser.quit()

    def signin_form(self, action):
        self.browser.get("%s%s" %
                         (str(self.live_server_url), '/accounts/login/'))
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')

        username_input.send_keys('test_login@example.com')
        password_input.send_keys('123test')
        if (action == "button"):
            submission_button = self.browser.find_element_by_class_name(
                'btn-success')
            submission_button.click()
        else:
            password_input.send_keys(Keys.ENTER)

        time.sleep(0.5)
        redirection_url = str(self.live_server_url) + '/'
        current_url = self.browser.current_url
        html = self.browser.page_source
        self.assertEqual(redirection_url,
                         current_url)
        self.assertInHTML("""
                    <h1 class="text-white-75">Du gras, oui, mais de qualité !</h1>
                        """,
                          html)

    def test_signin_with_button(self):
        self.signin_form('button')

    def test_signin_with_key(self):
        self.signin_form('key')

    def test_bad_signin(self):
        url_login = "%s%s" % (str(self.live_server_url), '/accounts/login/')
        self.browser.get(url_login)
        username_input = self.browser.find_element_by_id('id_username')
        password_input = self.browser.find_element_by_id('id_password')
        submission_button = self.browser.find_element_by_class_name(
            'btn-success')

        username_input.send_keys('test_login_bad@example.com')
        password_input.send_keys('123test')
        submission_button.click()

        time.sleep(0.5)
        html = self.browser.page_source
        self.assertEqual(url_login,
                         self.browser.current_url)
        self.assertInHTML("<h2>Connexion</h2>", html)
