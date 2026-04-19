from pages.sauce_demo.inventory_page import InventoryPage
from pages.sauce_demo.cart_page import CartPage
from pages.sauce_demo.checkout_info_page import CheckoutInfoPage
from pages.sauce_demo.checkout_overview_page import CheckoutOverviewPage
from playwright.sync_api import expect
#import pytest

# 1. THE HAPPY PATH: Full E2E Flow
def test_e2e_purchase_flow(page, config_data):
    """Verifies a user can successfully buy an item from start to finish."""
    inventory = InventoryPage(page)
    cart = CartPage(page)
    info = CheckoutInfoPage(page)
    overview = CheckoutOverviewPage(page)

    sd_data = config_data["sauce_demo"]
    customer = sd_data["customer_info"]
    product_name = sd_data["inventory_data"]["products"][0]["name"]

    # --- ACT ---
    inventory.navigate(sd_data["url"] + "inventory.html")
    inventory.add_item_to_cart_by_name(product_name)

    inventory.navigate(sd_data["url"] + "cart.html")
    cart.proceed_to_checkout()

    info.fill_checkout_info(
        customer["first_name"],
        customer["last_name"],
        customer["postal_code"]
    )

    overview.finish_checkout()

    # --- ASSERT ---
    expect(overview.complete_header).to_have_text("Thank you for your order!")


# 2. THE NEGATIVE TEST: Missing Data
def test_checkout_missing_info_error(page, config_data):
    """Verifies that the system prevents checkout if fields are empty."""
    inventory = InventoryPage(page)
    cart = CartPage(page)
    info = CheckoutInfoPage(page)
    url = config_data["sauce_demo"]["url"]

    # Arrange: Go to checkout info page
    inventory.navigate(url + "inventory.html")
    inventory.add_item_to_cart_by_index(0)
    inventory.navigate(url + "cart.html")
    cart.proceed_to_checkout()

    # Act: Click continue without filling anything
    info.click_element(info.btn_continue)

    # Assert: Verify error message is visible
    expect(info.error_message).to_be_visible()
    assert "Error: First Name is required" in info.get_error_message()


# 3. THE CALCULATED TEST: Price Validation
def test_checkout_price_math_validation(page, config_data):
    """Verifies that Item Total + Tax exactly equals the final Total."""
    inventory = InventoryPage(page)
    cart = CartPage(page)
    info = CheckoutInfoPage(page)
    overview = CheckoutOverviewPage(page)

    sd_data = config_data["sauce_demo"]
    customer = sd_data["customer_info"]

    # Arrange: Reach the Overview page
    inventory.navigate(sd_data["url"] + "inventory.html")
    inventory.add_item_to_cart_by_index(0)
    inventory.navigate(sd_data["url"] + "cart.html")
    cart.proceed_to_checkout()
    info.fill_checkout_info(customer["first_name"], customer["last_name"], customer["postal_code"])

    # Act: Extract prices from the UI
    # We split by '$' to get the number, e.g., 'Item total: $29.99' -> '29.99'
    item_total = float(overview.get_text(overview.item_total_label).split('$')[1])
    tax = float(overview.get_text(overview.tax_label).split('$')[1])
    actual_total = float(overview.get_text(overview.total_label).split('$')[1])

    # Assert: Math check
    expected_total = item_total + tax
    assert actual_total == expected_total, f"Expected {expected_total}, but got {actual_total}"