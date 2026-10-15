import re

from playwright.sync_api import Page


def product_slug(name: str) -> str:
    """'Sauce Labs Bolt T-Shirt' -> 'sauce-labs-bolt-t-shirt' (formato de los data-test)."""
    return re.sub(r"\s+", "-", name.strip().lower())


class InventoryPage:
    def __init__(self, page: Page):
        self.page = page
        self.title = page.get_by_test_id("title")
        self.items = page.get_by_test_id("inventory-item")
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.item_prices = page.get_by_test_id("inventory-item-price")
        self.sort_select = page.get_by_test_id("product-sort-container")
        self.cart_badge = page.get_by_test_id("shopping-cart-badge")
        self.cart_link = page.get_by_test_id("shopping-cart-link")
        self.menu_button = page.locator("#react-burger-menu-btn")
        self.logout_link = page.get_by_test_id("logout-sidebar-link")

    def add_to_cart(self, product: str):
        self.page.get_by_test_id(f"add-to-cart-{product_slug(product)}").click()

    def remove_from_cart(self, product: str):
        self.page.get_by_test_id(f"remove-{product_slug(product)}").click()

    def sort_by(self, label: str):
        self.sort_select.select_option(label=label)

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def prices(self) -> list[float]:
        return [float(p.replace("$", "")) for p in self.item_prices.all_inner_texts()]

    def go_to_cart(self):
        self.cart_link.click()

    def logout(self):
        self.menu_button.click()
        self.logout_link.click()
