# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

BDD end-to-end POC against https://www.saucedemo.com using Playwright (sync API, Python 3.13). The same `.feature` files run under **two runners**: behave and pytest-bdd (+ pytest-playwright). Feature files and step phrases are in **English** (Gherkin keywords and step text); code comments are in Spanish.

## Commands

Use the venv interpreter (`.venv/Scripts/python`); dependencies are pinned in `requirements.txt`.

```
.venv/Scripts/behave -n "Complete purchase"             # single scenario by name
.venv/Scripts/behave -D headed=true -D slowmo=500       # watch the browser; userdata defaults in behave.ini
.venv/Scripts/python -m pytest -k "complete_purchase"   # single scenario (scenario name, snake_case)
```

Any new Gherkin tag must be registered under `markers` in `pytest.ini`.

## Architecture

Shared by both runners: `features/*.feature` and `pages/`. Step implementations are **duplicated** with identical phrases — any step added or reworded in a feature must be implemented in both `features/steps/saucedemo_steps.py` (behave) and `tests/` (pytest-bdd). Run both suites after changes.

behave side:
- `features/steps/saucedemo_steps.py` — all steps (behave steps are global). Empty `Examples` values use the custom `{x:Text}` parse type.
- Data tables need a header row (behave treats row 1 as headings; pytest-bdd step skips it with `datatable[1:]`).

pytest-bdd side:
- Steps shared across features live in `tests/conftest.py`; put a step there as soon as a second feature needs it.
- `pages/` — Page Objects holding locators and actions; assertions (`expect`) live in steps, not in pages.

Conventions that are easy to break:

- A session-scoped autouse fixture sets Playwright's test-id attribute to `data-test`, so locators use `page.get_by_test_id("<data-test value>")`. Prefer that over CSS.
- pytest-bdd matches step type: a step used after `Given` in `Background` and after `When` in a scenario needs both `@given` and `@when` stacked on the same function.
- When an `Examples` value can be empty, use `parsers.re` with `[^"]*` instead of `parsers.parse` (`{x}` needs at least one char).
