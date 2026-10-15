from playwright.sync_api import Page


class CartPage:
    def __init__(self, page: Page):
        self.page = page
        self.item_names = page.get_by_test_id("inventory-item-name")
        self.checkout_button = page.get_by_test_id("checkout")

    def names(self) -> list[str]:
        return self.item_names.all_inner_texts()

    def checkout(self):
        self.checkout_button.click()
