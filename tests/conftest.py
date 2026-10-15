"""Fixtures y steps compartidos entre features."""
import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

import settings
from pages import CartPage, CheckoutPage, InventoryPage, LoginPage


def pytest_configure(config):
    # La URL viene del .env; un --base-url en la línea de comandos tiene prioridad
    if not config.option.base_url:
        config.option.base_url = settings.BASE_URL


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


@given("I am on the login page")
def open_login(login_page):
    login_page.open()


# Los valores pueden venir vacíos desde Examples, por eso se usa regex con [^"]*
@when(parsers.re(r'I log in with username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"'))
def do_login(login_page, username, password):
    login_page.login(username, password)


@given(parsers.parse('I am logged in as "{username}"'))
def logged_in_as(login_page, inventory_page, username):
    login_page.open()
    login_page.login(username, settings.PASSWORD)
    expect(inventory_page.title).to_have_text("Products")


# Registrado como given y when para poder usarlo tanto en Background como en escenarios
@given(parsers.parse('I add the product "{product}" to the cart'))
@when(parsers.parse('I add the product "{product}" to the cart'))
def add_to_cart(inventory_page, product):
    inventory_page.add_to_cart(product)


@given("I go to the cart")
@when("I go to the cart")
def go_to_cart(inventory_page):
    inventory_page.go_to_cart()


# Los valores pueden venir vacíos desde Examples, por eso se usa regex con [^"]*
@then(parsers.re(r'I see the error message "(?P<message>[^"]*)"'))
def error_message(page, message):
    expect(page.get_by_test_id("error")).to_have_text(message)
