import pytest
from playwright.sync_api import Page, expect

from uuid import uuid4

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
    page.goto("/")

    login_field = page.get_by_label("Username", exact=True)
    login_field.fill("admin")
    
    password_field = page.get_by_label("Password", exact=True)
    password_field.fill("admin")
    
    sign_in_button = page.get_by_role(role="button", name="Sign in", exact=True)
    sign_in_button.click()
    
    search_field = page.get_by_label("Search", exact=True)
    expect(search_field).to_be_visible()

    return page

@pytest.fixture
def test_project(authenticated_page: Page):
    project_name = f"UI project {uuid4().hex[:8]}"

    open_project_link = authenticated_page.get_by_role("link", name="New project", exact=True)
    expect(open_project_link).to_be_visible()
    open_project_link.click()

    name_field = authenticated_page.get_by_label("Name", exact=True)
    name_field.fill(project_name)

    save_button = authenticated_page.get_by_role(role="button", name="Save", exact=True)
    save_button.click()

    header = authenticated_page.locator(".title")
    expect(header).to_have_text(project_name)

    authenticated_page.wait_for_url("**/project/**")
    project_url = authenticated_page.url

    try:
        yield {
            "name": project_name,
            "url": project_url,
        }
    finally:
        authenticated_page.goto(project_url)
        remove_project_link = authenticated_page.get_by_role("link", name="Remove", exact=True)
        expect(remove_project_link).to_be_visible()
        remove_project_link.click()

        yes_button = authenticated_page.get_by_role(role="button", name="Yes", exact=True)
        yes_button.click()
        
        expect(authenticated_page.get_by_role("link", name=project_name, exact=True)).to_have_count(0)
