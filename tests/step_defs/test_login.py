import re

from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("login.feature")


@given("I am on the login page")
def open_login(login_page):
    login_page.open()


@when(parsers.re(r'I log in with username "(?P<username>[^"]*)" and password "(?P<password>[^"]*)"'))
def do_login(login_page, username, password):
    login_page.login(username, password)


@when("I log out")
def logout(inventory_page):
    inventory_page.logout()


@then("I see the products page")
def products_page(page, inventory_page):
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")


@then("I am back on the login page")
def back_to_login(login_page):
    expect(login_page.login_button).to_be_visible()
