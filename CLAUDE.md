# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Proyecto

POC de pruebas end-to-end BDD contra https://www.saucedemo.com usando Playwright (API sync, Python 3.13). Los mismos archivos `.feature` se ejecutan con **dos runners**: behave y pytest-bdd (+ pytest-playwright). Los features y las frases de los steps están en **inglés** (palabras clave de Gherkin y texto de los steps); los comentarios del código están en español.

## Comandos

Usar el intérprete del venv (`.venv/Scripts/python`); las dependencias están fijadas en `requirements.txt`.

```
.venv/Scripts/behave                                    # suite completa con behave
.venv/Scripts/python -m pytest                          # suite completa con pytest-bdd
.venv/Scripts/behave -n "Complete purchase"             # un escenario por nombre
.venv/Scripts/behave -D headed=false                    # sin navegador visible (behave.ini trae headed = true)
.venv/Scripts/python -m pytest -k "complete_purchase"   # un escenario (nombre del escenario en snake_case)
```

Todo tag nuevo de Gherkin debe registrarse en `markers` dentro de `pytest.ini`.

Ante una falla, behave guarda screenshot y trace en `test-results/behave/<escenario>/` y pytest en `test-results/pytest/` (pytest-playwright vacía su carpeta `--output` al iniciar; por eso no debe apuntar a `test-results/` o borra la evidencia de behave); se abre con `.venv/Scripts/playwright show-trace <ruta>/trace.zip`.

La URL base y la contraseña vienen del `.env` vía `settings.py` (ambos runners lo importan; si falta una variable se lanza un error al importar). El `.env` está en `.gitignore` — nunca subirlo al repo; toda variable nueva se agrega también a `.env.example`. En la línea de comandos, `--base-url` / `-D base_url=` tienen prioridad sobre el valor del `.env`.

## Arquitectura

Compartido por ambos runners: `features/*.feature` y `pages/` (Page Objects con localizadores y acciones; las aserciones (`expect`) van en los steps, no en las páginas). Las implementaciones de los steps están **duplicadas** con frases idénticas — todo step que se agregue o se reformule en un feature debe implementarse tanto en `features/steps/saucedemo_steps.py` (behave) como en `tests/` (pytest-bdd). Ejecutar ambas suites después de cada cambio.

El ciclo de vida de Playwright también está duplicado: behave crea browser/context/page y las instancias de los Page Objects sobre `context` en `features/environment.py`; pytest-bdd los obtiene de los fixtures de pytest-playwright más los fixtures de Page Objects en `tests/conftest.py`. Un Page Object nuevo debe exportarse en `pages/__init__.py` y conectarse en ambos lados.

Lado behave:
- `features/execution_log.py` — log por caso en `test-results/logs/<YYYYMMDD>/`, conectado desde los hooks de `environment.py` (`before_scenario`, `before_step`, `after_step`, `after_scenario`); usa el logger `saucedemo` sin propagar para que behave no lo capture.
- `features/steps/saucedemo_steps.py` — todos los steps (en behave los steps son globales). Los valores vacíos de `Examples` usan el tipo de parseo personalizado `{x:Text}`.
- Las tablas de datos necesitan fila de encabezado (behave toma la fila 1 como encabezados; el step de pytest-bdd la salta con `datatable[1:]`).

Lado pytest-bdd:
- Un `tests/step_defs/test_<feature>.py` por feature, que lo vincula con `scenarios("<feature>.feature")` — un `.feature` nuevo solo corre en pytest cuando existe este módulo.
- Los steps compartidos entre features van en `tests/conftest.py`; mover un step ahí apenas lo necesite un segundo feature.

Convenciones fáciles de romper:

- El atributo test-id de Playwright está configurado como `data-test` (pytest: fixture autouse de sesión; behave: `before_all`), por eso los localizadores usan `page.get_by_test_id("<valor de data-test>")`. Preferirlo sobre CSS.
- Cada `Scenario` / `Scenario Outline` empieza con un ID correlativo global: `QA_0001 Successful login ...`. Un escenario nuevo toma el siguiente número libre (buscar el mayor con `grep -o "QA_[0-9]*" features/*.feature`); los IDs no se reutilizan ni se renumeran. En un `Scenario Outline` cada fila es un caso propio: columna `case` (`01`, `02`…) en `Examples` y nombre `QA_NNNN_<case> ...` (ver `features/QA0002_login_errors.feature`). Los features nuevos se nombran `QANNNN_<nombre>.feature` con el ID de su escenario, y su módulo pytest `tests/step_defs/test_qannnn_<nombre>.py`. El ID queda en los nombres de pytest (`test_qa_0001_...`) y se filtra con `behave -n "QA_0001"` o `pytest -k qa_0001`.
- `I am logged in as "<user>"` solo indica el usuario; el step toma la contraseña real de `settings.PASSWORD`, así que no ponerla en los features.
- pytest-bdd distingue el tipo de step: un step usado después de `Given` en un `Background` y después de `When` en un escenario necesita `@given` y `@when` apilados sobre la misma función.
- Cuando un valor de `Examples` puede venir vacío, usar `parsers.re` con `[^"]*` en vez de `parsers.parse` (`{x}` necesita al menos un carácter).
