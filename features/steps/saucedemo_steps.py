"""Steps de behave para todas las features (en behave los steps son globales).

Usa las mismas frases que tests/step_defs/ (pytest-bdd): si cambias una, cambia ambas.
"""
import re

import parse
from behave import given, register_type, step, then, when
from playwright.sync_api import expect

PASSWORD = "secret_sauce"
SORT_RULES = {
    "Name (A to Z)": ("names", False),
    "Name (Z to A)": ("names", True),
    "Price (low to high)": ("prices", False),
    "Price (high to low)": ("prices", True),
}


# {x} de parse exige al menos un carácter; los Ejemplos tienen valores vacíos
@parse.with_pattern(r'[^"]*')
def parse_texto(text):
    return text


register_type(Texto=parse_texto)


# ---------- Compartidos ----------

@given('que inicié sesión como "{usuario}"')
def logged_in_as(context, usuario):
    context.login_page.open()
    context.login_page.login(usuario, PASSWORD)
    expect(context.inventory_page.title).to_have_text("Products")


@step('agrego al carrito el producto "{producto}"')
def add_to_cart(context, producto):
    context.inventory_page.add_to_cart(producto)


@step("voy al carrito")
def go_to_cart(context):
    context.inventory_page.go_to_cart()


@then('veo el mensaje de error "{mensaje:Texto}"')
def error_message(context, mensaje):
    expect(context.page.get_by_test_id("error")).to_have_text(mensaje)


# ---------- Login ----------

@given("que estoy en la página de login")
def open_login(context):
    context.login_page.open()


@when('inicio sesión con usuario "{usuario:Texto}" y contraseña "{clave:Texto}"')
def do_login(context, usuario, clave):
    context.login_page.login(usuario, clave)


@when("cierro sesión")
def logout(context):
    context.inventory_page.logout()


@then("veo la página de productos")
def products_page(context):
    expect(context.page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(context.inventory_page.title).to_have_text("Products")


@then("vuelvo a la página de login")
def back_to_login(context):
    expect(context.login_page.login_button).to_be_visible()


# ---------- Catálogo ----------

@then("veo {cantidad:d} productos en el catálogo")
def product_count(context, cantidad):
    expect(context.inventory_page.items).to_have_count(cantidad)


@when('ordeno los productos por "{orden}"')
def sort_products(context, orden):
    context.inventory_page.sort_by(orden)


@then('los productos quedan ordenados por "{orden}"')
def products_sorted(context, orden):
    field, reverse = SORT_RULES[orden]
    values = getattr(context.inventory_page, field)()
    assert values == sorted(values, reverse=reverse), f"Orden incorrecto para '{orden}': {values}"


# ---------- Carrito ----------

@when('quito del carrito el producto "{producto}"')
def remove_from_cart(context, producto):
    context.inventory_page.remove_from_cart(producto)


@then('el contador del carrito muestra "{cantidad}"')
def cart_badge(context, cantidad):
    expect(context.inventory_page.cart_badge).to_have_text(cantidad)


@then("el carrito contiene los productos:")
def cart_contains(context):
    expected = [row["producto"] for row in context.table]
    expect(context.cart_page.item_names).to_have_text(expected)


@then("el carrito está vacío")
def cart_empty(context):
    expect(context.inventory_page.cart_badge).to_have_count(0)


# ---------- Checkout ----------

@given("inicio el checkout")
def start_checkout(context):
    context.cart_page.checkout()


@when('ingreso nombre "{nombre:Texto}", apellido "{apellido:Texto}" y código postal "{cp:Texto}"')
def fill_info(context, nombre, apellido, cp):
    context.checkout_page.fill_info(nombre, apellido, cp)


@when("continúo al resumen de la compra")
def continue_to_overview(context):
    context.checkout_page.continue_to_overview()


@when("finalizo la compra")
def finish(context):
    context.checkout_page.finish()


@then('el total de la compra es "{total}"')
def order_total(context, total):
    expect(context.checkout_page.total).to_have_text(f"Total: {total}")


@then('veo el mensaje de confirmación "{mensaje}"')
def confirmation(context, mensaje):
    expect(context.checkout_page.complete_header).to_have_text(mensaje)
