class BasePage:
    def __init__(self, page):
        # We store the page object so all methods can use it via 'self'
        self.page = page

    def navigate(self, url: str):
        """Navigates to a specific URL."""
        self.page.goto(url)

    def click_element(self, locator):
        """Wait for element and click."""
        locator.click()

    def type_text(self, locator, text: str):
        """Clear and fill text into an input field."""
        locator.fill(text)

    def is_element_visible(self, locator) -> bool:
        """Check if an element is visible on the screen."""
        return locator.is_visible()

    def get_text(self, locator) -> str:
        """Retrieves text content from a locator."""
        return locator.inner_text()