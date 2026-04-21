from pages.base_page import BasePage

class OrangePIMPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # locators: using exact=False to handle extra spaces in OrangeHRM buttons
        self.pim_menu = page.get_by_role("link", name="PIM")
        self.add_button = page.get_by_role("button", name="Add", exact=False)

        # Add Employee Form
        self.first_name_input = page.get_by_placeholder("First Name")
        self.last_name_input = page.get_by_placeholder("Last Name")
        # FIXED: Changed "SAVE" to "Save" and added exact=False
        self.save_button = page.get_by_role("button", name="Save", exact=False)

        # Employee List / Search
        # FIXED: Corrected placeholder typo "foe" -> "for"
        self.employee_name_search = page.get_by_placeholder("Type for hints...").first
        self.search_button = page.get_by_role("button", name="Search")
        self.first_row_name = page.locator(".oxd-table-card").first

    def navigate_to_pim(self):
        """Navigate to the PIM page module from the sidebar"""
        self.pim_menu.click()

    def add_employee(self, first_name: str, last_name: str):
        """Standard workflow to create a new employee record."""
        self.add_button.click()
        self.first_name_input.fill(first_name)
        self.last_name_input.fill(last_name)
        self.save_button.click()
        # wait_for_load_state is okay, but targeted waits are better
        self.page.wait_for_load_state("networkidle")