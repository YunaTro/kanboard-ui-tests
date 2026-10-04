from playwright.sync_api import Page


class CreateTaskPage:
    def __init__(self, page: Page):
        self.page = page

        self.title_field = page.get_by_label("Title", exact=True)
        self.description_field = page.get_by_label("Description", exact=True)
        self.save_button = page.get_by_role("button", name="Save", exact=True)

    def create(self, title: str, description: str):
        self.title_field.fill(title)
        self.description_field.fill(description)
        self.save_button.click()