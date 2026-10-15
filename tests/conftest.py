"""Fixtures y steps compartidos entre features."""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

from pages import CartPage, CheckoutPage, InventoryPage, LoginPage

PASSWORD = "secret_sauce"


@pytest.fixture(scope="session", autouse=True)
def _data_test_attribute(playwright):
    # saucedemo usa data-test (no data-testid) -> get_by_test_id apunta a ese atributo
    playwright.selectors.set_test_id_attribute("data-test")


@pytest.fixture
def login_page(page):
    return LoginPage(page)


@pytest.fixture
def inventory_page(page):
    return InventoryPage(page)


@pytest.fixture
def cart_page(page):
    return CartPage(page)


@pytest.fixture
def checkout_page(page):
    return CheckoutPage(page)


@given(parsers.parse('que inicié sesión como "{usuario}"'))
def logged_in_as(login_page, inventory_page, usuario):
    login_page.open()
    login_page.login(usuario, PASSWORD)
    expect(inventory_page.title).to_have_text("Products")


# Registrado como given y when para poder usarlo tanto en Antecedentes como en escenarios
@given(parsers.parse('agrego al carrito el producto "{producto}"'))
@when(parsers.parse('agrego al carrito el producto "{producto}"'))
def add_to_cart(inventory_page, producto):
    inventory_page.add_to_cart(producto)


@given("voy al carrito")
@when("voy al carrito")
def go_to_cart(inventory_page):
    inventory_page.go_to_cart()


# Los valores pueden venir vacíos desde Ejemplos, por eso se usa regex con [^"]*
@then(parsers.re(r'veo el mensaje de error "(?P<mensaje>[^"]*)"'))
def error_message(page, mensaje):
    expect(page.get_by_test_id("error")).to_have_text(mensaje)
