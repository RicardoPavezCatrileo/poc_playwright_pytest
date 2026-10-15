from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("cart.feature")


@when(parsers.parse('quito del carrito el producto "{producto}"'))
def remove_from_cart(inventory_page, producto):
    inventory_page.remove_from_cart(producto)


@then(parsers.parse('el contador del carrito muestra "{cantidad}"'))
def cart_badge(inventory_page, cantidad):
    expect(inventory_page.cart_badge).to_have_text(cantidad)


@then("el carrito contiene los productos:")
def cart_contains(cart_page, datatable):
    expected = [row[0] for row in datatable[1:]]  # la primera fila es el encabezado
    expect(cart_page.item_names).to_have_text(expected)


@then("el carrito está vacío")
def cart_empty(inventory_page):
    expect(inventory_page.cart_badge).to_have_count(0)
