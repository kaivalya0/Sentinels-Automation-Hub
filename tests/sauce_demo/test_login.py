import pytest
from pages.sauce_demo.login_page import SauceLoginPage

@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.parametrize("user_index", [0, 1, 2])  # This will run the test 3 times
def test_valid_logins(page, config_data, user_index):
    login_page = SauceLoginPage(page)

    # 1. Get the URL and common password
    url = config_data["sauce_demo"]["url"]
    password = config_data["sauce_demo"]["common_password"]

    # 2. Pick the username from the LIST using the index
    username = config_data["sauce_demo"]["valid_users"][user_index]

    # 3. Act
    login_page.navigate(url)
    login_page.login_to_sauce(username, password)

    # 4. Assert
    assert "inventory.html" in page.url
    print(f"\n Login successful for user: {username}")


# This handles the list of 'invalid_users' from your JSON
@pytest.mark.regression
@pytest.mark.ui
@pytest.mark.parametrize("invalid_index", [0, 1])
def test_invalid_logins(page, config_data, invalid_index):
    login_page = SauceLoginPage(page)
    url = config_data["sauce_demo"]["url"]

    # Get user data from the 'invalid_users' list
    user_data = config_data["sauce_demo"]["invalid_users"][invalid_index]
    username = user_data["username"]
    password = user_data["password"]
    expected_error = user_data["error"]

    login_page.navigate(url)
    login_page.login_to_sauce(username, password)

    # Assert: Verify the error message contains the expected text from JSON
    actual_error = login_page.error_message.inner_text().lower()
    assert expected_error in actual_error
    print(f"\n  Negative test passed for: {username}")