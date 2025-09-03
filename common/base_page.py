import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC

DEFAULT_SLEEP_TIME = 0.005
DEFAULT_TIMEOUT = 10
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

    # Use Selenium XPath
    def click_element(self, locator: str, timeout: int=DEFAULT_TIMEOUT):
        element = self.wait_element_to_be_clickable(locator, timeout)
        element.click()

    def input_element(self, locator: str, text: str, timeout: int=DEFAULT_TIMEOUT):
        element = self.wait_element_to_be_clickable(locator, timeout)
        element.clear()
        element.send_keys(text)

    def clear_element(self, locator: str):
        self.driver.find_element(By.XPATH, locator).clear()

    def enter_element(self, locator: str):
        self.driver.find_element(By.XPATH, locator).send_keys(u"\ue007")  # Keys.ENTER

    def tab_element(self, locator: str):
        self.driver.find_element(By.XPATH, locator).send_keys(u"\ue004")  # Keys.TAB

    def wait_element_to_be_clickable(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((By.XPATH, locator))
        )

    def wait_element_to_be_visible(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.visibility_of_element_located((By.XPATH, locator))
        )

    def wait_element_to_be_hidden(self, locator: str, timeout: int = DEFAULT_TIMEOUT):
        return WebDriverWait(self.driver, timeout).until(
            EC.invisibility_of_element_located((By.XPATH, locator))
        )

    def waitForLoadState(self, timeout=DEFAULT_TIMEOUT):
        wait = WebDriverWait(self.driver, timeout)
        wait.until(lambda d: d.execute_script("return document.readyState") == "complete")
        wait.until(lambda d: d.find_element("tag name", "body"))

        def no_pending_requests(d):
            return d.execute_script("""
                return window.performance.getEntriesByType('resource')
                .filter(r => ['xmlhttprequest','fetch'].includes(r.initiatorType)).length
            """) == 0

        wait.until(no_pending_requests)

        return True

    def scroll_to_bottom(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_element(self, locator: str):
        el = self.driver.find_element(By.XPATH, locator)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", el)

    def refresh(self):
        self.driver.refresh()

    def clear_cache(self):
        self.driver.delete_all_cookies()
        self.driver.execute_script("window.localStorage.clear();")
        self.driver.execute_script("window.sessionStorage.clear();")

    def navigate_to(self, url: str):
        self.driver.get(url)

    def get_current_url(self) -> str:
        return self.driver.current_url

    def get_page_title(self) -> str:
        return self.driver.title

    def get_page_source(self) -> str:
        return self.driver.page_source

    def get_element_text(self, locator: str) -> str:
        return self.driver.find_element(By.XPATH, locator).text

    def get_element_attribute(self, locator: str, attribute: str) -> str:
        return self.driver.find_element(By.XPATH, locator).get_attribute(attribute)

    def count_elements(self, locator: str) -> int:
        return len(self.driver.find_elements(By.XPATH, locator))

    def is_element_present(self, locator: str) -> bool:
        return len(self.driver.find_elements(By.XPATH, locator)) > 0

    def is_element_enabled(self, locator: str) -> bool:
        return self.driver.find_element(By.XPATH, locator).is_enabled()

    def is_element_disabled(self, locator: str) -> bool:
        return not self.driver.find_element(By.XPATH, locator).is_enabled()

    def select_by_visible_text(self, locator: str, text: str):
        select = Select(self.driver.find_element(By.XPATH, locator))
        select.select_by_visible_text(text)

    def select_by_value(self, locator: str, value: str):
        select = Select(self.driver.find_element(By.XPATH, locator))
        select.select_by_value(value)

    def select_by_index(self, locator: str, index: int):
        select = Select(self.driver.find_element(By.XPATH, locator))
        select.select_by_index(index)

    def zoom_browser(self, zoom_percentage=DEFAULT_ZOOM_PERCENT):
        self.driver.execute_script(f"document.body.style.zoom='{zoom_percentage}%'")
        self.driver.execute_script("document.body.style.overflow='auto';")

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
