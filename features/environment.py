"""Hooks de behave: ciclo de vida de Playwright (equivalente a pytest-playwright + tests/conftest.py)."""
import re
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))  # para importar pages/ al ejecutar el script `behave`

from pages import CartPage, CheckoutPage, InventoryPage, LoginPage  # noqa: E402

RESULTS_DIR = ROOT / "test-results" / "behave"


def before_all(context):
    userdata = context.config.userdata
    context.base_url = userdata.get("base_url")
    context.playwright = sync_playwright().start()
    # saucedemo usa data-test (no data-testid) -> get_by_test_id apunta a ese atributo
    context.playwright.selectors.set_test_id_attribute("data-test")
    browser_type = getattr(context.playwright, userdata.get("browser", "chromium"))
    context.browser = browser_type.launch(
        headless=not userdata.getbool("headed", False),
        slow_mo=userdata.getfloat("slowmo", 0),
    )


def before_scenario(context, scenario):
    context.browser_context = context.browser.new_context(base_url=context.base_url)
    context.browser_context.tracing.start(screenshots=True, snapshots=True)
    context.page = context.browser_context.new_page()
    context.login_page = LoginPage(context.page)
    context.inventory_page = InventoryPage(context.page)
    context.cart_page = CartPage(context.page)
    context.checkout_page = CheckoutPage(context.page)


def after_scenario(context, scenario):
    if scenario.status == "failed":
        out = RESULTS_DIR / re.sub(r"[^\w-]+", "_", scenario.name).strip("_")
        out.mkdir(parents=True, exist_ok=True)
        context.page.screenshot(path=str(out / "screenshot.png"), full_page=True)
        context.browser_context.tracing.stop(path=str(out / "trace.zip"))
    else:
        context.browser_context.tracing.stop()
    context.browser_context.close()


def after_all(context):
    context.browser.close()
    context.playwright.stop()
