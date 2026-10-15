from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("inventory.feature")

SORT_RULES = {
    "Name (A to Z)": ("names", False),
    "Name (Z to A)": ("names", True),
    "Price (low to high)": ("prices", False),
    "Price (high to low)": ("prices", True),
}


@then(parsers.parse("veo {cantidad:d} productos en el catálogo"))
def product_count(inventory_page, cantidad):
    expect(inventory_page.items).to_have_count(cantidad)


@when(parsers.parse('ordeno los productos por "{orden}"'))
def sort_products(inventory_page, orden):
    inventory_page.sort_by(orden)


@then(parsers.parse('los productos quedan ordenados por "{orden}"'))
def products_sorted(inventory_page, orden):
    field, reverse = SORT_RULES[orden]
    values = getattr(inventory_page, field)()
    assert values == sorted(values, reverse=reverse), f"Orden incorrecto para '{orden}': {values}"
