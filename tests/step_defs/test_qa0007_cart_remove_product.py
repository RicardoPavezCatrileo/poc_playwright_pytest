from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("QA0007_cart_remove_product.feature")


@when(parsers.parse('I remove the product "{product}" from the cart'))
def remove_from_cart(inventory_page, product):
    inventory_page.remove_from_cart(product)


@then("the cart is empty")
def cart_empty(inventory_page):
    expect(inventory_page.cart_badge).to_have_count(0)
