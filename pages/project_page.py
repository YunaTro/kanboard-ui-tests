from playwright.sync_api import Page


class ProjectPage:
    def __init__(self, page: Page):
        self.page = page

        self.configure_link = page.get_by_role("link", name="Configure this project")
        self.add_task_link = page.get_by_role("link", name="Add a new task")
        self.list_link = page.get_by_role(role="link", name="List", exact=True)
        self.task_links = page.locator("span.table-list-title a[href*='/task/']")
        self.remove_link = page.get_by_role("link", name="Remove", exact=True)
        self.confirm_remove_button = page.get_by_role(role="button", name="Yes", exact=True)
        self.header = page.locator(".title")

    def open(self, url: str):
        self.page.goto(url)

    def open_settings(self):
        self.configure_link.click()

    def open_task_creation(self):
        self.add_task_link.click()

    def open_task_list(self):
        self.list_link.click()
    
    def open_task(self, title: str):
        task_link = self.task_links.and_(
            self.page.get_by_role(
                "link",
                name=title,
                exact=True,
            )
        )
        task_link.click()

    def delete(self):
        self.remove_link.click()
        self.confirm_remove_button.click()
