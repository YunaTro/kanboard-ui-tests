from playwright.sync_api import Page

class LoginPage:
    def __init__(self, page: Page):
        self.page = page

        self.username_field = page.get_by_label("Username", exact=True)
        self.password_field = page.get_by_label("Password", exact=True)
        self.sign_in_button = page.get_by_role(role="button", name="Sign in", exact=True)
        self.invalid_credentials_message = page.get_by_text("Bad username or password", exact=True)

    def open(self):
        self.page.goto("/")

    def login(self, username: str, password: str):
        self.username_field.fill(username)
        self.password_field.fill(password)
        self.sign_in_button.click()
    