import pytest
import re
from playwright.sync_api import Page, expect
from pages.orange_hrm.pim_page import OrangePIMPage

def test_add_new_employee(page: Page, config_data):
    # 1. Arrange
    pim = OrangePIMPage(page)
    url = config_data["orange_hrm"]["url"]
    f_name, l_name = "Automation", "Tester"

    # 2. Act
    # We navigate directly to the list to bypass side-menu clicking for speed
    pim.navigate(f"{url}web/index.php/pim/viewEmployeeList")
    pim.add_employee(f_name, l_name)

    # 3. Assert
    # Verify redirection to the employee personal details page
    expect(page).to_have_url(
        re.compile(r".*/pim/viewPersonalDetails/empNumber/.*"),
        timeout=15000
    )
    # Verify the header shows the new name
    expect(page.get_by_role("heading", name=f"{f_name} {l_name}")).to_be_visible()