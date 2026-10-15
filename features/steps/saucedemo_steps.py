"""Steps de behave para todas las features (en behave los steps son globales).

Usa las mismas frases que tests/step_defs/ (pytest-bdd): si cambias una, cambia ambas.
"""
import re

import parse
from behave import given, register_type, step, then, when
from playwright.sync_api import expect

import settings

SORT_RULES = {
    "Name (A to Z)": ("names", False),
    "Name (Z to A)": ("names", True),
    "Price (low to high)": ("prices", False),
    "Price (high to low)": ("prices", True),
}


# {x} de parse exige al menos un carácter; los Examples tienen valores vacíos
@parse.with_pattern(r'[^"]*')
def parse_text(text):
    return text


register_type(Text=parse_text)


# ---------- Compartidos ----------

@given('I am logged in as "{username}"')
def logged_in_as(context, username):
    context.login_page.open()
    context.login_page.login(username, settings.PASSWORD)
    expect(context.inventory_page.title).to_have_text("Products")


@step('I add the product "{product}" to the cart')
def add_to_cart(context, product):
    context.inventory_page.add_to_cart(product)


@step("I go to the cart")
def go_to_cart(context):
    context.inventory_page.go_to_cart()


@then('I see the error message "{message:Text}"')
def error_message(context, message):
    expect(context.page.get_by_test_id("error")).to_have_text(message)


# ---------- Login ----------

@given("I am on the login page")
def open_login(context):
    context.login_page.open()


@when('I log in with username "{username:Text}" and password "{password:Text}"')
def do_login(context, username, password):
    context.login_page.login(username, password)


@when("I log out")
def logout(context):
    context.inventory_page.logout()


@then("I see the products page")
def products_page(context):
    expect(context.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(context.inventory_page.title).to_have_text("Products")


@then("I am back on the login page")
def back_to_login(context):
    expect(context.login_page.login_button).to_be_visible()


# ---------- Catálogo ----------

@then("I see {count:d} products in the catalog")
def product_count(context, count):
    expect(context.inventory_page.items).to_have_count(count)


@when('I sort the products by "{order}"')
def sort_products(context, order):
    context.inventory_page.sort_by(order)


@then('the products are sorted by "{order}"')
def products_sorted(context, order):
    field, reverse = SORT_RULES[order]
    values = getattr(context.inventory_page, field)()
    assert values == sorted(values, reverse=reverse), f"Orden incorrecto para '{order}': {values}"


# ---------- Carrito ----------

@when('I remove the product "{product}" from the cart')
def remove_from_cart(context, product):
    context.inventory_page.remove_from_cart(product)


@then('the cart badge shows "{count}"')
def cart_badge(context, count):
    expect(context.inventory_page.cart_badge).to_have_text(count)


@then("the cart contains the products:")
def cart_contains(context):
    expected = [row["product"] for row in context.table]
    expect(context.cart_page.item_names).to_have_text(expected)


@then("the cart is empty")
def cart_empty(context):
    expect(context.inventory_page.cart_badge).to_have_count(0)


# ---------- Checkout ----------

@given("I start the checkout")
def start_checkout(context):
    context.cart_page.checkout()


@when('I enter first name "{first_name:Text}", last name "{last_name:Text}" and postal code "{postal_code:Text}"')
def fill_info(context, first_name, last_name, postal_code):
    context.checkout_page.fill_info(first_name, last_name, postal_code)


@when("I continue to the order overview")
def continue_to_overview(context):
    context.checkout_page.continue_to_overview()


@when("I finish the purchase")
def finish(context):
    context.checkout_page.finish()


@then('the order total is "{total}"')
def order_total(context, total):
    expect(context.checkout_page.total).to_have_text(f"Total: {total}")


@then('I see the confirmation message "{message}"')
def confirmation(context, message):
    expect(context.checkout_page.complete_header).to_have_text(message)
