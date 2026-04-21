from pages.base_page import BasePage

class OrangeLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Using Playwright's recommended locators
        self.username_input = page.get_by_placeholder("Username")
        self.password_input = page.get_by_placeholder("Password")
        self.login_button = page.get_by_role("button", name="Login")
        self.error_msg = page.get_by_role("alert")

    def login(self, username, password):
        """Standard login flow"""
        self.username_input.fill(username)
        self.password_input.fill(password)
        self.login_button.click()

    def get_error_text(self):
        """Captures invalid credential messages"""
        return self.error_msg.inner_text()