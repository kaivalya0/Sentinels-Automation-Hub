from playwright.sync_api import expect
from pages.base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Standardized Pro Locators
        self.header_title = page.get_by_role("heading", name="Your Cart")
        self.cart_item = page.locator("[data-test='inventory-item']")
        self.btn_checkout = page.get_by_role("button", name="Checkout")
        self.item_name = page.locator("[data-test='inventory-item-name']")
        self.item_price = page.locator("[data-test='inventory-item-price']")

    def verify_on_cart_page(self):
        """Gatekeeper check for page load."""
        expect(self.header_title).to_be_visible()

    def get_item_details(self):
        """
        Returns name and price of the first item in the cart.
        Uses the base_page utility to fetch text safely.
        """
        return {
            "name": self.get_text(self.item_name.first),
            "price": self.get_text(self.item_price.first)
        }

    def verify_item_visible(self, item_name: str):
        """New Standard: Uses Playwright assertions for validation."""
        expect(self.page.get_by_text(item_name)).to_be_visible()

    def proceed_to_checkout(self):
        self.btn_checkout.click()