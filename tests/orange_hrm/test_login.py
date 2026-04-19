import pytest
import re  # ✅ ADD THIS LINE
from playwright.sync_api import Page, expect
from pages.orange_hrm.login_page import OrangeLoginPage


def test_login_successful(page: Page, config_data):
    """
    Validates the standard login flow for OrangeHRM.
    Uses 'config_data' fixture from conftest.py.
    """
    # 1. Arrange
    login_page = OrangeLoginPage(page)
    data = config_data["orange_hrm"]

    # 2. Act
    login_page.navigate(data["url"])
    login_page.login(
        data["admin_user"]["username"],
        data["admin_user"]["password"]
    )

    # 3. Assert
    # Verify redirection to dashboard
    expect(page).to_have_url(re.compile(r".*/dashboard/index"))
    # Verify the Dashboard header is visible via our Page Object
    # (Assuming you added a dashboard check to your Page Object)
    expect(page.get_by_role("heading", name="Dashboard")).to_be_visible()


def test_login_invalid_credentials(page: Page, config_data):
    """Checks the UI reaction to bad credentials."""
    # 1. Arrange
    login_page = OrangeLoginPage(page)
    data = config_data["orange_hrm"]

    # 2. Act
    login_page.navigate(data["url"])
    login_page.login("InvalidUser", "WrongPassword")

    # 3. Assert
    # Check for the 'Invalid credentials' toast/alert
    expect(login_page.error_msg).to_be_visible()
    assert "Invalid credentials" in login_page.get_error_text()