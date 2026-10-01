from playwright.sync_api import Page, expect
from uuid import uuid4

def test_created_task_is_preserved_after_reload(authenticated_page, test_project):
    authenticated_page.goto(test_project["url"])

    settings_link = authenticated_page.get_by_role("link", name="Configure this project")
    settings_link.click()

    new_task_link = authenticated_page.get_by_role("link", name="Add a new task")
    new_task_link.click()

    task_name = f"UI task {uuid4().hex[:8]}"
    task_desc = "This is a UI task for training QA-project"

    title_field = authenticated_page.get_by_label("Title", exact=True)
    title_field.fill(task_name)

    desc_field = authenticated_page.get_by_label("Description", exact=True)
    desc_field.fill(task_desc)

    save_button = authenticated_page.get_by_role(role="button", name="Save", exact=True)
    save_button.click()

    list_link = authenticated_page.get_by_role(role="link", name="List", exact=True)
    list_link.click()

    task_link = authenticated_page.get_by_role("link", name=task_name, exact=True)
    task_link.click()

    task_title = authenticated_page.locator("#task-summary h2")
    expect(task_title).to_have_text(task_name)

    task_description = authenticated_page.locator(".accordion-content .markdown p")
    expect(task_description).to_have_text(task_desc)

    authenticated_page.reload()
    expect(task_title).to_have_text(task_name)
    expect(task_description).to_have_text(task_desc)
