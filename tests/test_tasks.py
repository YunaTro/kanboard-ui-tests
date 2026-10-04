from playwright.sync_api import expect
from uuid import uuid4

from pages.create_task_page import CreateTaskPage
from pages.task_page import TaskPage
from pages.project_page import ProjectPage

def test_created_task_is_preserved_after_reload(authenticated_page, test_project):
    project = ProjectPage(authenticated_page)
    project.open(test_project["url"])
    project.open_settings()
    project.open_task_creation()

    task_name = f"UI task {uuid4().hex[:8]}"
    task_desc = "This is a UI task for training QA-project"

    task_form = CreateTaskPage(authenticated_page)
    task_form.create(task_name, task_desc)

    project.open_task_list()
    project.open_task(task_name)

    task = TaskPage(authenticated_page)
    expect(task.title).to_have_text(task_name)
    expect(task.description).to_have_text(task_desc)

    task.reload()
    expect(task.title).to_have_text(task_name)
    expect(task.description).to_have_text(task_desc)
