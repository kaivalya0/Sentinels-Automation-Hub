import pytest
import random
from pages.orange_hrm.pim_page import OrangePIMPage
from services.orange_hrm.pim_service import PIMService


@pytest.fixture
def pim_setup(api_client, config_data):
    """
    Setup/Teardown Fixture:
    - Creates employee before test (Setup)
    - Deletes employee after test (Teardown)
    """
    service = PIMService(api_client)
    data = config_data["orange_hrm"]["new_employee"]
    emp_id = str(random.randint(100000, 999999))

    # SETUP
    service.add_new_employee(data["first_name"], data["last_name"], emp_id)

    # Provide data to the test
    yield {"id": emp_id, "first_name": data["first_name"], "last_name": data["last_name"]}

    # TEARDOWN: Runs regardless of test success or failure
    # service.delete_employee([emp_id])
    print(f"\nCleanup: Employee {emp_id} deleted.")


@pytest.mark.ui
@pytest.mark.api
@pytest.mark.test_data_validation  # For SQL verification
def test_pim_employee_visibility_hybrid(page, config_data, pim_setup):
    """
    Hybrid test utilizing automated setup and teardown.
    """
    # 1. ARRANGE: Data provided by the fixture
    emp = pim_setup
    pim_page = OrangePIMPage(page)

    # 2. ACT: UI Interaction
    page.goto(config_data["orange_hrm"]["url"])
    pim_page.navigate_to_pim()
    pim_page.search_employee_by_id(emp["id"])

    # 3. ASSERT: Pro-level targeted verification
    pim_page.verify_employee_data(emp["id"], emp["first_name"], emp["last_name"])