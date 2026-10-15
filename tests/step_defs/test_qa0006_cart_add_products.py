from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then

scenarios("QA0006_cart_add_products.feature")


@then(parsers.parse('the cart badge shows "{count}"'))
def cart_badge(inventory_page, count):
    expect(inventory_page.cart_badge).to_have_text(count)


@then("the cart contains the products:")
def cart_contains(cart_page, datatable):
    expected = [row[0] for row in datatable[1:]]  # la primera fila es el encabezado
    expect(cart_page.item_names).to_have_text(expected)
