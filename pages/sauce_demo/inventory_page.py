from pages.base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Selectors
        self.header_title = page.locator("[data-test='title']")
        self.inventory_item = page.locator("[data-test='inventory-item']")
        self.cart_badge = page.locator("[data-test='shopping-cart-badge']")
        # Store the button selector as a string for use in sub-locators
        self.btn_add_to_cart = "button:has-text('Add to cart')"
        self.btn_menu = page.locator("#react-burger-menu-btn")
        self.btn_logout = page.locator("#logout_sidebar_link")
        

    def add_item_to_cart_by_name(self, item_name: str):
        """
        Finds a specific product card by name and clicks its button.
        Demonstrates the AAA (Arrange-Act-Assert) pattern.
        """
        # Logic: Isolate the parent container (the card) first
        target_item = self.inventory_item.filter(has_text=item_name)

        # Act: Click the button INSIDE that specific card
        target_item.locator(self.btn_add_to_cart).click()

    def get_header_text(self):
        """Retrieves page title for verification."""
        return self.get_text(self.header_title)

    def is_at_inventory_page(self):
        """Check if the landing page is correct."""
        return self.is_element_visible(self.header_title)

    def add_item_to_cart_by_index(self, index: int = 0):
        """Brittle method: kept for legacy or quick checks."""
        item = self.inventory_item.nth(index)
        item.locator(self.btn_add_to_cart).click()

    def get_cart_count(self):
        """Validation for cart badge changes."""
        if self.is_element_visible(self.cart_badge):
            return self.get_text(self.cart_badge)
        return "0"

    def logout(self):
        """Action: Opens sidebar and clicks logout."""
        self.btn_menu.click()
        self.btn_logout.click()