import re
import pytest
from playwright.sync_api import Page, expect
from pages.orange_hrm.pim_page import OrangePIMPage

@pytest.mark.smoke
@pytest.mark.ui
def test_add_new_employee(page: Page, config_data):
    # 1. Arrange - Setup POM and pull dynamic data
    pim = OrangePIMPage(page)
    url = config_data["orange_hrm"]["url"]

    # Accessing flattened structure: config_data['orange_hrm']['new_employee']
    employee_info = config_data["orange_hrm"]["new_employee"]
    f_name = employee_info["first_name"]
    l_name = employee_info["last_name"]

    # 2. Act - Strategic navigation to save CI execution time
    pim.navigate(f"{url}web/index.php/pim/viewEmployeeList")
    pim.add_employee(f_name, l_name)

    # 3. Assert - Long timeout to handle slow OrangeHRM demo server responses
    expect(page).to_have_url(
        re.compile(r".*/pim/viewPersonalDetails/empNumber/.*"),
        timeout=15000
    )