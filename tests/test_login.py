from playwright.sync_api import Page, expect


def test_login_form_is_available(page: Page):
    page.goto("/")

    login_field = page.get_by_label("Username", exact=True)
    expect(login_field).to_be_visible()
    expect(login_field).to_be_editable()

    password_field = page.get_by_label("Password", exact=True)
    expect(password_field).to_be_visible()
    expect(password_field).to_be_editable()
    expect(password_field).to_have_attribute("type", "password")

    sign_in_button = page.get_by_role(role="button", name="Sign in", exact=True)
    expect(sign_in_button).to_be_visible()
    expect(sign_in_button).to_be_enabled()

def test_user_can_log_in_with_valid_credentials(page: Page):
    page.goto("/")

    login_field = page.get_by_label("Username", exact=True)
    login_field.fill("admin")

    password_field = page.get_by_label("Password", exact=True)
    password_field.fill("admin")

    sign_in_button = page.get_by_role(role="button", name="Sign in", exact=True)
    sign_in_button.click()

    search_field = page.get_by_label("Search", exact=True)
    expect(search_field).to_be_visible()
    page.reload()
    expect(search_field).to_be_visible()

def test_login_with_invalid_password_shows_error(page: Page):
    page.goto("/")
    login_field = page.get_by_label("Username", exact=True)
    login_field.fill("admin")

    password_field = page.get_by_label("Password", exact=True)
    password_field.fill("wrong")

    sign_in_button = page.get_by_role(role="button", name="Sign in", exact=True)
    sign_in_button.click()

    error_message = page.get_by_text("Bad username or password", exact=True)
    expect(error_message).to_be_visible()

    expect(login_field).to_be_editable()
    expect(password_field).to_be_editable()
