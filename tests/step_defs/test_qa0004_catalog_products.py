from playwright.sync_api import expect
from pytest_bdd import parsers, scenarios, then

scenarios("QA0004_catalog_products.feature")


@then(parsers.parse("I see {count:d} products in the catalog"))
def product_count(inventory_page, count):
    expect(inventory_page.items).to_have_count(count)
