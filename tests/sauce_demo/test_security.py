from pages.sauce_demo.inventory_page import InventoryPage
from playwright.sync_api import expect


def test_logout_security_gate(page, config_data):
    inventory = InventoryPage(page)
    url = config_data["sauce_demo"]["url"]

    # Arrange: Start at inventory
    inventory.navigate(url + "inventory.html")

    # Act: Logout
    inventory.logout()

    # Assert: Try to go back to inventory directly
    page.goto(url + "inventory.html")

    # ✅ SECURITY GATE: Should be redirected back to login
    expect(page).to_have_url(url)
    print("\n✅ Security: Session successfully destroyed after logout.")