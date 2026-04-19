from pages.base_page import BasePage

class CheckoutInfoPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # ✅ Professional Locators: Using data-test attributes for 100% stability
        self.first_name_field = page.locator("[data-test='firstName']")
        self.last_name_field = page.locator("[data-test='lastName']")
        self.postal_code_field = page.locator("[data-test='postalCode']")
        self.btn_continue = page.locator("[data-test='continue']")
        self.btn_cancel = page.locator("[data-test='cancel']")
        self.error_message = page.locator("[data-test='error']")

    def fill_checkout_info(self, f_name: str, l_name: str, zip_code: str):
        """
        Action: Fills the entire checkout form in one go.
        This represents a 'Macro' action for better test readability.
        """
        self.first_name_field.fill(f_name)
        self.last_name_field.fill(l_name)
        self.postal_code_field.fill(zip_code)
        self.click_element(self.btn_continue)

    def get_error_message(self):
        """Used for Negative Testing: Verify error appears when fields are empty."""
        return self.get_text(self.error_message)