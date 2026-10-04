from playwright.sync_api import Page, expect
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage

def test_login_form_is_available(login_page):
    login_page.open()

    expect(login_page.username_field).to_be_visible()
    expect(login_page.username_field).to_be_editable()

    expect(login_page.password_field).to_be_visible()
    expect(login_page.password_field).to_be_editable()
    expect(login_page.password_field).to_have_attribute("type", "password")

    expect(login_page.sign_in_button).to_be_visible()
    expect(login_page.sign_in_button).to_be_enabled()

def test_user_can_log_in_with_valid_credentials(page: Page):
    login = LoginPage(page)
    login.open()
    login.login(username="admin", password="admin")
    
    dashboard = DashboardPage(page)
    expect(dashboard.search_field).to_be_visible()
    dashboard.reload()
    expect(dashboard.search_field).to_be_visible()

def test_login_with_invalid_password_shows_error(login_page: LoginPage):
    login_page.open()
    login_page.login(username="admin", password="wrong")

    expect(login_page.invalid_credentials_message).to_be_visible()

    expect(login_page.username_field).to_be_editable()
    expect(login_page.password_field).to_be_editable()
