import time

DEFAULT_SLEEP_TIME = 0.005
DEFAULT_TIMEOUT = 0
DEFAULT_ZOOM_PERCENT = 100


class BasePage:
    def __init__(self, driver):
        self.driver = driver

    @staticmethod
    def sleep(t=DEFAULT_SLEEP_TIME):
        time.sleep(t)

    @staticmethod
    def format_locator(locator_template, value):
        return locator_template.format(value)

    # Use Playwright CSS Selector
    def click_element(self, locator: str):
        self.driver.locator(locator).click()

    def input_element(self, locator: str, text: str):
        self.driver.locator(locator).fill(text)

    def clear_element(self, locator: str):
        self.driver.locator(locator).fill("")

    def enter_element(self, locator: str):
        self.driver.locator(locator).press('Enter')

    def tab_element(self, locator: str):
        self.driver.locator(locator).press('Tab')

    def wait_element_to_be_clickable(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return self.driver.locator(locator).wait_for(state="attached", timeout=timeout)

    def wait_element_to_be_visible(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return self.driver.locator(locator).wait_for(state="visible", timeout=timeout)

    def wait_element_to_be_hidden(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return self.driver.locator(locator).wait_for(state="hidden", timeout=timeout)

    def scroll_to_bottom(self):
        self.driver.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_element(self, locator: str):
        element = self.driver.locator(locator)
        element.scroll_into_view_if_needed()

    def refresh(self):
        self.driver.reload()

    def clear_cache(self):
        context = self.driver.context
        context.clear_cookies()
        self.driver.evaluate("window.localStorage.clear();")
        self.driver.evaluate("window.sessionStorage.clear();")

    def navigate_to(self, url: str):
        self.driver.goto(url)

    def get_current_url(self) -> str:
        return self.driver.url

    def get_page_title(self) -> str:
        return self.driver.title()

    def get_page_source(self) -> str:
        return self.driver.content()

    def get_element_text(self, locator: str) -> str:
        return self.driver.locator(locator).text_content()

    def get_element_attribute(self, locator: str, attribute: str) -> str:
        return self.driver.locator(locator).get_attribute(attribute)

    def count_elements(self, locator: str) -> int:
        return self.driver.locator(locator).count()

    def is_element_present(self, locator: str) -> bool:
        return self.driver.locator(locator).count() > 0

    def is_element_enabled(self, locator: str) -> bool:
        return self.driver.locator(locator).is_enabled()

    def is_element_disabled(self, locator: str) -> bool:
        return not self.driver.locator(locator).is_enabled()

    def select_by_visible_text(self, locator: str, text: str):
        self.driver.locator(locator).select_option(label=text)

    def select_by_value(self, locator: str, value: str):
        self.driver.locator(locator).select_option(value=value)

    def select_by_index(self, locator: str, index: int):
        self.driver.locator(locator).select_option(index=index)

    def zoom_browser(self, zoom_percentage=DEFAULT_ZOOM_PERCENT):
        self.driver.evaluate(f"document.body.style.zoom = '{zoom_percentage}%'")
        self.driver.evaluate("document.body.style.overflow = 'auto';")

    # Use Beautiful Soup
    def soup_get_page_title(self, soup):
        return soup.title.string if soup.title else None

    def soup_get_element_text(self, soup, selector):
        element = soup.select_one(selector)
        return element.get_text(strip=True) if element else None

    def soup_get_element_attribute(self, soup, selector, attribute):
        element = soup.select_one(selector)
        return element.get(attribute) if element else None

    def soup_count_elements(self, soup, selector):
        return len(soup.select(selector))

    def soup_check_element_existed(self, soup, selector):
        return soup.select_one(selector) is not None

    def soup_check_element_enabled(self, soup, selector):
        element = soup.select_one(selector)
        return bool(element and not element.has_attr('disabled'))

    def soup_check_element_disabled(self, soup, selector):
        element = soup.select_one(selector)
        return bool(element and element.has_attr('disabled'))

    def soup_select_dropbox_by_visible_text(self, soup, selector, text):
        for option in soup.select(f'{selector} option'):
            if option.get_text(strip=True) == text:
                return option.get('value')
        return None

    def soup_select_dropbox_by_value(self, soup, selector, value):
        for option in soup.select(f'{selector} option'):
            if option.get('value') == value:
                return option.get_text(strip=True)
        return None

    def soup_select_dropbox_by_index(self, soup, selector, index):
        options = soup.select(f'{selector} option')
        if 0 <= index < len(options):
            option = options[index]
            return option.get_text(strip=True), option.get('value')
        return None
