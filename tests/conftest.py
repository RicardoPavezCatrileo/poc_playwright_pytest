"""Fixtures y steps compartidos entre features."""
import re
from pathlib import Path

import pytest
from playwright.sync_api import expect
from pytest_bdd import given, parsers, then, when

import settings
from pages import CartPage, CheckoutPage, InventoryPage, LoginPage

FEATURES_DIR = Path(__file__).resolve().parent.parent / "features"


def pytest_configure(config):
    # La URL viene del .env; un --base-url en la línea de comandos tiene prioridad
    if not config.option.base_url:
        config.option.base_url = settings.BASE_URL
    # Los tags de caso (@QA_0001, @QA_0002_01...) se registran solos leyendo los features
    qa_tags = set()
    for feature in FEATURES_DIR.glob("*.feature"):
        qa_tags.update(re.findall(r"@(QA_\d+(?:_\d+)?)\b", feature.read_text(encoding="utf-8")))
    for tag in sorted(qa_tags):
        config.addinivalue_line("markers", f"{tag}: caso de prueba {tag}")


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


@given("I start the checkout")
def start_checkout(cart_page):
    cart_page.checkout()


@when(parsers.re(
    r'I enter first name "(?P<first_name>[^"]*)", last name "(?P<last_name>[^"]*)"'
    r' and postal code "(?P<postal_code>[^"]*)"'
))
def fill_info(checkout_page, first_name, last_name, postal_code):
    checkout_page.fill_info(first_name, last_name, postal_code)


@when("I continue to the order overview")
def continue_to_overview(checkout_page):
    checkout_page.continue_to_overview()


# Los valores pueden venir vacíos desde Examples, por eso se usa regex con [^"]*
@then(parsers.re(r'I see the error message "(?P<message>[^"]*)"'))
def error_message(page, message):
    expect(page.get_by_test_id("error")).to_have_text(message)
