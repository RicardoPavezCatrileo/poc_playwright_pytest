import re

from playwright.sync_api import expect
from pytest_bdd import scenarios, then

scenarios("QA0001_login_success.feature")


@then("I see the products page")
def products_page(page, inventory_page):
    expect(page).to_have_url(re.compile(r"/inventory\.html$"))
    expect(inventory_page.title).to_have_text("Products")
