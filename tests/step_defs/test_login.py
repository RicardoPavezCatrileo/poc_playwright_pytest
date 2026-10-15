import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("login.feature")


@given("que estoy en la página de login")
def open_login(login_page):
    login_page.open()


@when(parsers.re(r'inicio sesión con usuario "(?P<usuario>[^"]*)" y contraseña "(?P<clave>[^"]*)"'))
def do_login(login_page, usuario, clave):
    login_page.login(usuario, clave)


@when("cierro sesión")
def logout(inventory_page):
    inventory_page.logout()


@then("veo la página de productos")
def products_page(page, inventory_page):
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")


@then("vuelvo a la página de login")
def back_to_login(login_page):
    expect(login_page.login_button).to_be_visible()
