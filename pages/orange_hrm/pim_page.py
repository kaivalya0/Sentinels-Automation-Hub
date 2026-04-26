from playwright.sync_api import expect
from pages.base_page import BasePage


class OrangePIMPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # --- Sidebar & Navigation ---
        self.pim_menu = page.get_by_role("link", name="PIM")

        # --- Locators for Employee Creation (UI-based) ---
        self.add_button = page.get_by_role("button", name="Add", exact=False)
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        self.save_button = page.get_by_role("button", name="Save", exact=False)

        # --- Locators for Search & Verification ---
        self.id_search_field = page.locator("div.oxd-input-group:has-text('Employee Id') input")
        self.search_button = page.get_by_role("button", name="Search")

    def navigate(self, url: str):
        """Direct URL navigation ."""
        self.page.goto(url)

    def navigate_to_pim(self):
        """Sidebar-based navigation."""
        self.pim_menu.click()

    def add_employee(self, first_name: str, last_name: str):
        """
        Completes the UI form to add an employee.
        Used by tests/orange_hrm/test_pim.py .
        """
        self.add_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.save_button.click()
        self.page.wait_for_load_state("networkidle")

    def search_employee_by_id(self, employee_id: str):
        """Filters the table by ID ."""
        self.id_search_field.fill(employee_id)
        self.search_button.click()
        self.page.wait_for_load_state("networkidle")

    def verify_employee_data(self, emp_id: str, first_name: str, last_name: str):
        """Targeted row-level verification ."""
        target_row = self.page.locator(".oxd-table-card").filter(has_text=emp_id)
        expect(target_row).to_contain_text(first_name)
        expect(target_row).to_contain_text(last_name)