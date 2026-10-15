from playwright.sync_api import expect
from pytest_bdd import scenarios, then, when

scenarios("QA0003_logout.feature")


@when("I log out")
def logout(inventory_page):
    inventory_page.logout()


@then("I am back on the login page")
def back_to_login(login_page):
    expect(login_page.login_button).to_be_visible()
