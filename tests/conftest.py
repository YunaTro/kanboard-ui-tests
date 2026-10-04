import pytest
from playwright.sync_api import Page, expect

from uuid import uuid4
from pages.login_page import LoginPage
from pages.dashboard_page import DashboardPage
from pages.create_project_page import CreateProjectPage
from pages.project_page import ProjectPage

@pytest.fixture
def login_page(page: Page):
    return LoginPage(page)

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {
            "width": 1440,
            "height": 900,
        },
    }

@pytest.fixture
def authenticated_page(page: Page):
    login = LoginPage(page)
    login.open()
    login.login(username="admin", password="admin")
    
    dashboard = DashboardPage(page)
    expect(dashboard.search_field).to_be_visible()

    return page

@pytest.fixture
def test_project(authenticated_page: Page):
    project_name = f"UI project {uuid4().hex[:8]}"

    dashboard = DashboardPage(authenticated_page)
    expect(dashboard.open_project_link).to_be_visible()
    dashboard.open_project_creation()

    project_form = CreateProjectPage(authenticated_page)
    project_form.create(project_name)

    authenticated_page.wait_for_url("**/project/**")
    project_url = authenticated_page.url
    project = ProjectPage(authenticated_page)

    try:
        expect(project.header).to_have_text(project_name)
        yield {
            "name": project_name,
            "url": project_url,
        }
    finally:
        project.open(project_url)
        project.delete()

        expect(dashboard.search_field).to_be_visible()
        expect(dashboard.find_project_by_name(project_name)).to_have_count(0)
