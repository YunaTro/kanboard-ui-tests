# Kanboard UI Tests

An educational UI test automation project for [Kanboard](https://kanboard.org/), a self-hosted project management application. The suite covers authentication and a task creation workflow using Python, pytest, and Playwright.

## Tech Stack

- Python
- pytest and pytest-playwright
- Playwright synchronous API with Chromium
- Docker Compose for the local Kanboard environment

## Test Coverage

| Scenario | Checks |
| --- | --- |
| Login form | Username and password fields are visible and editable; the password input uses the correct type; the sign-in button is enabled. |
| Successful login | The authenticated interface appears and remains accessible after a page reload. |
| Invalid password | An authentication error is displayed and the login fields remain editable. |
| Task creation | A task is created in a temporary project; its title and description match the submitted values before and after a page reload. |

Project creation and deletion support test setup and cleanup; they are not separate feature tests. The suite does not cover task editing, permissions, or multiple browsers.

## Test Design

- Each UI test uses an isolated browser context provided by pytest-playwright.
- Shared fixtures configure the browser and prepare an authenticated page.
- The task fixture creates a uniquely named project and attempts to remove it during teardown, including when a test assertion fails.
- Unique task names distinguish data created by each run.
- Locators use accessible roles, labels, and CSS selectors.
- Playwright auto-waiting and retrying `expect` assertions replace fixed delays.
- Screenshots are saved on test failure.

## Project Structure

- `conftest.py`: browser settings, authentication, and temporary project fixtures.
- `test_login.py`: login form and authentication checks.
- `test_tasks.py`: task creation and persistence checks.
- `compose.yaml`: local application configuration and persistent data volume.
- `pytest.ini`: test discovery, browser, base URL, and failure artifact settings.

## Prerequisites

- Python with `pip` and `venv`, compatible with the versions in `requirements.txt`.
- Docker with Docker Compose support; Docker must be running.
- An available local port `8080`.

The test environment uses Kanboard `v1.2.45`, as pinned in `compose.yaml`. Tests expect an English interface and the local account `admin` / `admin`. If the account details have been changed, update the authentication fixture and relevant login tests.

## Setup

Clone this repository or download it, then open a terminal in its root directory. Run all commands below from that directory.

### 1. Create a virtual environment

```bash
python -m venv .venv
```

Activate it using the command for your shell:

**Linux**

```bash
source .venv/bin/activate
```

### 2. Install dependencies and Chromium

```bash
python -m pip install -r requirements.txt
python -m playwright install chromium
```

### 3. Start Kanboard

```bash
docker compose up -d
docker compose ps
```

Open [http://localhost:8080](http://localhost:8080) and wait until the login form is available before running tests. No manually created project is required.

If the application does not start, inspect its logs:

```bash
docker compose logs --tail=50 kanboard
```

## Running Tests

Run the full suite in headless mode:

```bash
python -m pytest -v
```

Run with a visible browser:

```bash
python -m pytest -v --headed
```

Run authentication tests:

```bash
python -m pytest tests/test_login.py -v
```

Run only the task creation scenario:

```bash
python -m pytest tests/test_tasks.py::test_created_task_is_preserved_after_reload -v
```

The base URL is configured in `pytest.ini`. To use another compatible test instance:

```bash
python -m pytest -v --base-url http://localhost:8081
```

## Failure Artifacts

The pytest configuration enables `--screenshot only-on-failure` and saves artifacts under `test-results/`. Inspect the screenshot together with the pytest traceback to understand the page state at failure.

Generated artifacts, virtual environments, and cache directories are excluded from version control.

## Test Data and Cleanup

Task tests create temporary projects and tasks through the UI. Project teardown removes the temporary project and its tasks. If setup or cleanup is interrupted, leftover projects can be identified by the `UI project` prefix and reviewed manually.

Run the suite against a dedicated test instance: it creates and deletes application data.

## Stopping the Application

```bash
docker compose down
```

The named Docker volume preserves application data between starts.

## Test Architecture

UI interactions are organized using the Page Object pattern. Each class groups locators and actions for a specific screen or workflow:

- `LoginPage` — login form interactions.
- `DashboardPage` — dashboard elements and navigation to project creation.
- `CreateProjectPage` — project creation form.
- `ProjectPage` — project navigation, task selection, and project deletion.
- `CreateTaskPage` — task creation form.
- `TaskPage` — task details and page reload.

Tests describe user scenarios and verify outcomes with Playwright’s `expect` assertions. Page Objects encapsulate interface details, while pytest fixtures manage authentication and temporary test data.

Each task scenario uses a separate project with a unique name. The project fixture performs cleanup in a `finally` block, including when a test assertion fails.

Page Objects reuse the Playwright `Page` supplied by fixtures and preserve its built-in auto-waiting behavior. The refactoring retains the existing checks for login, invalid credentials, and task persistence after reload.