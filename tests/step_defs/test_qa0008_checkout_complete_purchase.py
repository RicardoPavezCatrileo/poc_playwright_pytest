from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then, when

scenarios("QA0008_checkout_complete_purchase.feature")


@when("I finish the purchase")
def finish(checkout_page):
    checkout_page.finish()


@then(parsers.parse('the order total is "{total}"'))
def order_total(checkout_page, total):
    expect(checkout_page.total).to_have_text(f"Total: {total}")


@then(parsers.parse('I see the confirmation message "{message}"'))
def confirmation(checkout_page, message):
    expect(checkout_page.complete_header).to_have_text(message)
