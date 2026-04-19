import pytest
from pages.sauce_demo.inventory_page import InventoryPage
from playwright.sync_api import expect


def test_verify_inventory_access(page, config_data):
    """Verifies that we can access inventory via stored session."""
    inventory = InventoryPage(page)
    url = config_data["sauce_demo"]["url"] + "inventory.html"

    inventory.navigate(url)

    # Assert header is visible (Proves auth.json worked!)
    expect(inventory.header_title).to_be_visible()
    assert inventory.get_header_text() == "Products"