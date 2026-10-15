from pytest_bdd import parsers, scenarios, then, when

scenarios("QA0005_sort_products.feature")

SORT_RULES = {
    "Name (A to Z)": ("names", False),
    "Name (Z to A)": ("names", True),
    "Price (low to high)": ("prices", False),
    "Price (high to low)": ("prices", True),
}


@when(parsers.parse('I sort the products by "{order}"'))
def sort_products(inventory_page, order):
    inventory_page.sort_by(order)


@then(parsers.parse('the products are sorted by "{order}"'))
def products_sorted(inventory_page, order):
    field, reverse = SORT_RULES[order]
    values = getattr(inventory_page, field)()
    assert values == sorted(values, reverse=reverse), f"Orden incorrecto para '{order}': {values}"
