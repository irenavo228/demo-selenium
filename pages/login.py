from common.base_page import BasePage
from locators.login import LoginLocator


class LoginPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def login(self, usr, pwd):
        self.click_element("a#login2")
        self.clear_element(LoginLocator.TXT_USER)
        self.input_element(LoginLocator.TXT_USER, usr)
        self.clear_element(LoginLocator.TXT_PASS)
        self.input_element(LoginLocator.TXT_PASS, pwd)
        self.click_element(LoginLocator.BTN_LOGIN)

    def check_title(self, text):
        self.wait_element_to_be_visible(LoginLocator.TXT_TITLE)
        assert self.get_element_text(LoginLocator.TXT_TITLE) == text
