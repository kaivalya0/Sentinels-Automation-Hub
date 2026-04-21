from pages.base_page import BasePage

class CheckoutOverviewPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        # Professional Locators
        self.btn_finish = page.locator("[data-test='finish']")
        self.btn_cancel = page.locator("[data-test='cancel']")
        self.item_total_label = page.locator("[data-test='subtotal-label']")
        self.tax_label = page.locator("[data-test='tax-label']")
        self.total_label = page.locator("[data-test='total-label']")
        # Final success elements
        self.complete_header = page.locator("[data-test='complete-header']")

    def finish_checkout(self):
        """Action: Finalizes the order."""
        self.click_element(self.btn_finish)

    def get_order_complete_text(self):
        """Validation: Returns the 'THANK YOU' message."""
        return self.get_text(self.complete_header)

    def get_item_total(self):
        """Returns the 'Item total: $X.XX' string."""
        return self.get_text(self.item_total_label)

    def get_tax(self):
        """Returns the 'Tax: $X.XX' string."""
        return self.get_text(self.tax_label)

    def get_total(self):
        """Returns the 'Total: $X.XX' string."""
        return self.get_text(self.total_label)