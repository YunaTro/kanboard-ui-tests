from playwright.sync_api import Page


class TaskPage:
    def __init__(self, page: Page):
        self.page = page

        self.title = page.locator("#task-summary h2")
        self.description = page.locator(".accordion-content .markdown p")
    
    def reload(self):
        self.page.reload()