import pytest

pytestmark = pytest.mark.order(1)


class TestLogin:

    def test_login(self, setup_web, setup_pages, data_login):
        _, base_url, _, _ = setup_web
        base_test = setup_pages
        login_page = base_test.get_page("login_page")

        ip_username = data_login['ip_username']
        ip_password = data_login['ip_password']
        op_title = data_login['op_title']

        login_page.login(ip_username, ip_password)
        login_page.check_title(op_title)
