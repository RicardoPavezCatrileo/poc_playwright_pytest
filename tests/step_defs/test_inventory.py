from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("inventory.feature")

SORT_RULES = {
    "Name (A to Z)": ("names", False),
    "Name (Z to A)": ("names", True),
    "Price (low to high)": ("prices", False),
    "Price (high to low)": ("prices", True),
}


@then(parsers.parse("I see {count:d} products in the catalog"))
def product_count(inventory_page, count):
    expect(inventory_page.items).to_have_count(count)


@when(parsers.parse('I sort the products by "{order}"'))
def sort_products(inventory_page, order):
    inventory_page.sort_by(order)


@then(parsers.parse('the products are sorted by "{order}"'))
def products_sorted(inventory_page, order):
    field, reverse = SORT_RULES[order]
    values = getattr(inventory_page, field)()
    assert values == sorted(values, reverse=reverse), f"Orden incorrecto para '{order}': {values}"
