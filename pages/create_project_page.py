from playwright.sync_api import Page


class CreateProjectPage:
    def __init__(self, page: Page):
        self.page = page

        self.name_field = page.get_by_label("Name", exact=True)
        self.save_button = page.get_by_role("button", name="Save", exact=True)

    def create(self, name: str):
        self.name_field.fill(name)
        self.save_button.click()