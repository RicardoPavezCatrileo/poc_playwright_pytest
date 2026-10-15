from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("cart.feature")


@when(parsers.parse('I remove the product "{product}" from the cart'))
def remove_from_cart(inventory_page, product):
    inventory_page.remove_from_cart(product)


@then(parsers.parse('the cart badge shows "{count}"'))
def cart_badge(inventory_page, count):
    expect(inventory_page.cart_badge).to_have_text(count)


@then("the cart contains the products:")
def cart_contains(cart_page, datatable):
    expected = [row[0] for row in datatable[1:]]  # la primera fila es el encabezado
    expect(cart_page.item_names).to_have_text(expected)


@then("the cart is empty")
def cart_empty(inventory_page):
    expect(inventory_page.cart_badge).to_have_count(0)
