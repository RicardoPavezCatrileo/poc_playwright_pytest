from playwright.sync_api import expect
from pytest_bdd import given, parsers, scenarios, then, when

scenarios("checkout.feature")


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


@when("I finish the purchase")
def finish(checkout_page):
    checkout_page.finish()


@then(parsers.parse('the order total is "{total}"'))
def order_total(checkout_page, total):
    expect(checkout_page.total).to_have_text(f"Total: {total}")


@then(parsers.parse('I see the confirmation message "{message}"'))
def confirmation(checkout_page, message):
    expect(checkout_page.complete_header).to_have_text(message)
