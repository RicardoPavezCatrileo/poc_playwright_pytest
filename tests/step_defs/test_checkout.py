from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("checkout.feature")


@given("inicio el checkout")
def start_checkout(cart_page):
    cart_page.checkout()


@when(parsers.re(
    r'ingreso nombre "(?P<nombre>[^"]*)", apellido "(?P<apellido>[^"]*)" y código postal "(?P<cp>[^"]*)"'
))
def fill_info(checkout_page, nombre, apellido, cp):
    checkout_page.fill_info(nombre, apellido, cp)


@when("continúo al resumen de la compra")
def continue_to_overview(checkout_page):
    checkout_page.continue_to_overview()


@when("finalizo la compra")
def finish(checkout_page):
    checkout_page.finish()


@then(parsers.parse('el total de la compra es "{total}"'))
def order_total(checkout_page, total):
    expect(checkout_page.total).to_have_text(f"Total: {total}")


@then(parsers.parse('veo el mensaje de confirmación "{mensaje}"'))
def confirmation(checkout_page, mensaje):
    expect(checkout_page.complete_header).to_have_text(mensaje)
