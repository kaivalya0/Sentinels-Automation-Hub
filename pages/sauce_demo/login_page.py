from pages.base_page import BasePage

class SauceLoginPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # ✅ FIX: SauceDemo uses lowercase placeholders or better yet, data-test IDs
        self.username_field = page.locator("[data-test='username']")
        self.password_field = page.locator("[data-test='password']")
        self.login_button = page.locator("[data-test='login-button']")
        self.error_message = page.locator("[data-test='error']")

    def navigate(self, url):
        """Navigate to the SauceDemo URL."""
        self.page.goto(url)

    def login_to_sauce(self, user, pwd):
        """Performs the login action using BasePage methods."""
        # ✅ FIX: Using your BasePage wrapper methods (Great job!)
        self.type_text(self.username_field, user)
        self.type_text(self.password_field, pwd)
        self.click_element(self.login_button)