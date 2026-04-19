
from pages.sauce_demo.inventory_page import InventoryPage
from pages.sauce_demo.cart_page import CartPage
from playwright.sync_api import expect


def test_add_to_cart_and_verify(page, config_data):
    inventory = InventoryPage(page)
    cart = CartPage(page)
    url = config_data["sauce_demo"]["url"]

    # 1. Arrange: Go to Inventory (Session bypasses login)
    inventory.navigate(url + "inventory.html")

    # 2. Act: Add a specific item from JSON
    product_to_add = config_data["sauce_demo"]["inventory_data"]["products"][0]["name"]
    inventory.add_item_to_cart_by_name(product_to_add)
    inventory.navigate(url + "cart.html")

    # 3. Assert: Verify Cart State
    details = cart.get_item_details()
    assert details["name"] == product_to_add
    expect(cart.cart_item).to_have_count(1)

    print(f"\n✅ Cart verified: {details['name']} is present at {details['price']}")