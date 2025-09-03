from pages.login import LoginPage


class BaseTest:
    def __init__(self, driver):
        self.driver = driver

    def get_page(self, page_name):
        pages = {
            "login_page": LoginPage(self.driver)
        }

        if page_name not in pages:
            raise ValueError(f"Page '{page_name}' is not defined in BaseTest.")
        return pages[page_name]
