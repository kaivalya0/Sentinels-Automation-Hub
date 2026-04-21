from pages.base_page import BasePage

class CartPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        #  Standardized locators
        self.header_title = page.locator("[data-test='title']")
        self.cart_item = page.locator("[data-test='inventory-item']")
        self.item_name = page.locator("[data-test='inventory-item-name']")
        self.item_price = page.locator("[data-test='inventory-item-price']")
        self.btn_checkout = page.locator("[data-test='checkout']")

    def get_item_details(self):
        """Returns name and price of the first item in the cart."""
        return {
            "name": self.get_text(self.item_name.first),
            "price": self.get_text(self.item_price.first)
        }

    def proceed_to_checkout(self):
        """Action: Clicks the checkout button to move to the Information page."""
        self.click_element(self.btn_checkout)