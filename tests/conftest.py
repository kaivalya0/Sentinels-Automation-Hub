
import pytest
import json
import os
import time
import allure
from pathlib import Path
from filelock import FileLock
from dotenv import load_dotenv
from utils.api_client import APIClient

ROOT_DIR = Path(__file__).parent.parent
DATA_DIR = ROOT_DIR / "data"
load_dotenv(dotenv_path=ROOT_DIR / ".env")

AUTH_FILES = {
    "sauce_demo": DATA_DIR / "auth_sauce.json",
    "orange_hrm": DATA_DIR / "auth_orange.json"
}

SESSION_TIMEOUT = 86400

@pytest.fixture(scope="session")
def config_data():
    data_path = DATA_DIR / "test_data.json"
    with open(data_path) as f:
        data = json.load(f)
    data["orange_hrm"]["admin_user"]["username"] = os.getenv("ORANGE_ADMIN_USER", data["orange_hrm"]["admin_user"]["username"])
    data["orange_hrm"]["admin_user"]["password"] = os.getenv("ORANGE_ADMIN_PASS", data["orange_hrm"]["admin_user"]["password"])
    data["sauce_demo"]["common_password"] = os.getenv("SAUCE_PASS", data["sauce_demo"]["common_password"])
    return data

@pytest.fixture(scope="function")
def browser_context_args(browser_type, config_data, tmp_path_factory, request):
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    nodeid = request.node.nodeid
    target_app = "orange_hrm" if "orange_hrm" in nodeid else "sauce_demo"
    auth_file = AUTH_FILES[target_app]
    lock_file = tmp_path_factory.getbasetemp().parent / f"{target_app}.lock"
    with FileLock(str(lock_file)):
        if auth_file.exists() and (time.time() - os.path.getmtime(auth_file) > SESSION_TIMEOUT):
            os.remove(auth_file)
        if not auth_file.exists():
            _generate_session(browser_type, config_data, target_app, auth_file)
    if "test_login" in nodeid:
        return {}
    return {"storage_state": str(auth_file)}

def _generate_session(browser_type, config, app_name, target_path):
    browser = browser_type.launch(headless=True)
    context = browser.new_context()
    page = context.new_page()
    data = config[app_name]
    page.goto(data["url"])
    if app_name == "sauce_demo":
        page.get_by_placeholder("Username").fill(data["valid_users"][0])
        page.get_by_placeholder("Password").fill(data["common_password"])
        page.get_by_role("button", name="Login").click()
        page.wait_for_url("**/inventory.html")
    elif app_name == "orange_hrm":
        page.get_by_placeholder("Username").fill(data["admin_user"]["username"])
        page.get_by_placeholder("Password").fill(data["admin_user"]["password"])
        page.get_by_role("button", name="Login").click()
        #  FIX: Wait for URL transition before looking for elements
        page.wait_for_url("**/dashboard/index", timeout=20000)
        page.get_by_text("Dashboard").first.wait_for(state="visible", timeout=15000)
    context.storage_state(path=str(target_path))
    browser.close()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    # This only triggers on 'call' failures, not 'setup' errors
    if report.when == "call" and report.failed:
        page = item.funcargs.get("page")
        if page:
            allure.attach(page.screenshot(full_page=True), name=f"FAILED_{item.name}", attachment_type=allure.attachment_type.PNG)
            Path("reports/screenshots").mkdir(parents=True, exist_ok=True)
            page.screenshot(path=f"reports/screenshots/{item.name}.png")


@pytest.fixture(scope="function")
def api_client(playwright, config_data, request):
    """
    Reuses the storage state for API calls.
    Now the API client is 'logged in' automatically.
    """
    nodeid = request.node.nodeid
    target_app = "orange_hrm" if "orange_hrm" in nodeid else "sauce_demo"
    auth_file = AUTH_FILES[target_app]

    # Create context using the same auth file generated in browser_context_args
    request_context = playwright.request.new_context(
        base_url=config_data[target_app]["url"],
        storage_state=str(auth_file) if auth_file.exists() else None
    )

    client = APIClient(request_context)
    yield client
    request_context.dispose()  # Clean up to prevent memory leaks