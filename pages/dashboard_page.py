from playwright.sync_api import Page

class DashboardPage:
    def __init__(self, page: Page):
        self.page = page
        self.search_field = page.get_by_label("Search", exact=True)
        self.open_project_link = page.get_by_role("link", name="New project", exact=True)
    
    def open_project_creation(self):
        self.open_project_link.click()
    
    def reload(self):
        self.page.reload()

    def find_project_by_name(self, name: str):
        return self.page.get_by_role("link", name=name, exact=True)