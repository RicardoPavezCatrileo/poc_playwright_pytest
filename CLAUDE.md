# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

BDD end-to-end POC against https://www.saucedemo.com using pytest-bdd + pytest-playwright (sync API, Python 3.13). Feature files and step text are written in **Spanish** (`# language: es` → `Característica`, `Antecedentes`, `Escenario`, `Esquema del escenario`, `Ejemplos`, `Dado/Cuando/Entonces/Y`). Keep new features and step phrases in Spanish.

## Commands

Use the venv interpreter (`.venv/Scripts/python`); dependencies are pinned in `requirements.txt`.

```
.venv/Scripts/python -m pytest                          # full suite
.venv/Scripts/python -m pytest -m smoke                 # Gherkin tags become pytest markers
.venv/Scripts/python -m pytest -k "compra_completa"     # single scenario (scenario name, snake_case)
.venv/Scripts/python -m pytest --headed --slowmo 500    # watch the browser
```

`pytest.ini` already sets `--base-url`, chromium, and screenshot/trace on failure into `test-results/`. Any new Gherkin tag must be registered under `markers` in `pytest.ini`.

## Architecture

- `features/*.feature` — scenarios. `bdd_features_base_dir = features/`, so step modules call `scenarios("login.feature")` with paths relative to that folder.
- `tests/step_defs/test_<feature>.py` — one module per feature: binds the feature and defines steps only that feature uses.
- `tests/conftest.py` — Page Object fixtures (`login_page`, `inventory_page`, `cart_page`, `checkout_page`) and steps shared across features (login as user, add to cart, go to cart, error message). Put a step here as soon as a second feature needs it.
- `pages/` — Page Objects holding locators and actions; assertions (`expect`) live in steps, not in pages.

Conventions that are easy to break:

- A session-scoped autouse fixture sets Playwright's test-id attribute to `data-test`, so locators use `page.get_by_test_id("<data-test value>")`. Prefer that over CSS.
- pytest-bdd matches step type: a step used after `Dado` in `Antecedentes` and after `Cuando` in a scenario needs both `@given` and `@when` stacked on the same function.
- When an `Ejemplos` value can be empty, use `parsers.re` with `[^"]*` instead of `parsers.parse` (`{x}` needs at least one char).
- Product add/remove buttons are located by slug (`add-to-cart-sauce-labs-backpack`); see `product_slug` in `pages/inventory_page.py`.
- Shared password for all saucedemo users is `secret_sauce` (`PASSWORD` in `tests/conftest.py`).
