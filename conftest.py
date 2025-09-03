import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService

from pages.login import LoginPage
from common.base_test import BaseTest
from utils.helpers import get_full_path, load_config, read_csv

web_conf = get_full_path("configs/web_conf.json")
test_results = {}


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", help="Choose browser: chrome, firefox")
    parser.addoption("--env", action="store", default="local", help="Choose environment: local, sit, uat, prod")
    parser.addoption("--mode", action="store", default="headless", help="Choose mode: head, headless")


def pytest_generate_tests(metafunc):
    env = metafunc.config.getoption("env")
    base_folder = os.path.join("data", env)
    test_file_name = metafunc.definition.fspath.basename
    csv_file_name = test_file_name.replace("test_", "").replace(".py", ".csv")
    csv_file_path = os.path.join(base_folder, csv_file_name)

    if not os.path.exists(base_folder):
        raise FileNotFoundError(f"Environment folder '{base_folder}' does not exist.")

    if not os.path.exists(csv_file_path):
        raise FileNotFoundError(f"No CSV file found for test '{test_file_name}' in folder '{base_folder}'.")

    data = read_csv(csv_file_path)
    for arg in metafunc.fixturenames:
        if arg.startswith("data_"):
            metafunc.parametrize(arg, data)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item):
    outcome = yield
    report = outcome.get_result()
    code = None
    result = "SKIPPED"

    if hasattr(item, "callspec"):
        params = item.callspec.params
        code = next((value["code"] for key, value in params.items() if isinstance(value, dict) and "code" in value),
                    None)

    if report.when in ["setup", "teardown"]:
        return

    if code:
        item.user_properties.append(("code", code))
        error_message = str(report.longrepr)

        if error_message != "None":
            result = "FAILED"
            print(f"ERROR in test case {code}: {error_message}")
        elif report.outcome == "passed":
            result = "PASSED"

        test_results[code] = result
        print(f"Code={code}, Result={result}")


@pytest.fixture(scope="session")
def get_driver(request):
    browser_name = request.config.getoption("--browser").lower()
    mode_conf = request.config.getoption("--mode")

    driver = None

    if browser_name == "chrome":
        options = ChromeOptions()
        if mode_conf == "headless":
            options.add_argument("--headless")
            options.add_argument("--disable-gpu")
            options.add_argument("--no-sandbox")

        driver_path = get_full_path("drivers/chromedriver.exe") # Windows
        # driver_path = "/usr/local/bin/chromedriver"  # Linux/Mac

        service = ChromeService(executable_path=driver_path)
        driver = webdriver.Chrome(service=service, options=options)

    elif browser_name == "firefox":
        options = FirefoxOptions()
        if mode_conf == "headless":
            options.add_argument("--headless")

        driver_path = get_full_path("drivers/geckodriver.exe")  # Windows
        # driver_path = "/usr/local/bin/geckodriver"  # Linux/Mac

        service = FirefoxService(executable_path=driver_path)
        driver = webdriver.Firefox(service=service, options=options)

    else:
        raise ValueError(f"Unsupported browser: {browser_name}")

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def get_source(request):
    env_conf = request.config.getoption("--env")
    web = load_config(web_conf, env_conf)
    yield web


@pytest.fixture(scope="session")
def setup_web(get_driver, get_source):
    driver = get_driver
    web = get_source
    driver.get(web["base_url"])
    yield driver, web["base_url"], web["usr"], web["pwd"]


@pytest.fixture(scope="session")
def setup_pages(get_driver):
    yield BaseTest(get_driver)


@pytest.fixture(scope="session")
def login_once(setup_web):
    driver, base_url, usr, pwd = setup_web
    login_page = LoginPage(driver)
    login_page.login(usr, pwd)
    yield driver, base_url, login_page.get_current_url()
