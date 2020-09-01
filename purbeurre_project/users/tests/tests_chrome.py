import time

from django.test import LiveServerTestCase

from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys


class SignupTest(LiveServerTestCase):

    def setUp(self):
        self.browser = Chrome()

    def tearDown(self):
        self.browser.quit()

    def test_signup(self):
        # Open a selenium browser & retrieve the forms elements we want to test
        self.browser.get(str(self.live_server_url) + '/accounts/signup/')
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
        submission_button.click()
        time.sleep(6)
        redirection_url = self.browser.current_url

        self.assertEqual(str(self.live_server_url) + "/accounts/login/",
                         redirection_url)
