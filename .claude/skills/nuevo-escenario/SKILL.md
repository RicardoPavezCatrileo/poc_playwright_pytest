---
name: nuevo-escenario
description: Agregar o modificar un escenario, step o feature de Gherkin en este POC manteniendo sincronizados los dos runners (behave y pytest-bdd). Usar siempre que se cree o cambie un .feature, una frase de step, un tag o un Page Object.
---

# Nuevo escenario (behave + pytest-bdd)

En este proyecto cada frase de Gherkin se implementa **dos veces**, con texto idéntico. Un cambio
solo está terminado cuando las dos suites pasan.

## 1. Escribir o editar el `.feature`

- Archivo en `features/<feature>.feature`. Keywords **y** texto de los steps en **inglés**.
- **ID obligatorio:** el nombre de cada `Scenario` / `Scenario Outline` empieza con `QA_NNNN`
  (ej. `Scenario: QA_0010 Add product from detail page`). El número es correlativo global entre
  todos los features: tomar el mayor existente (`grep -o "QA_[0-9]*" features/*.feature`) y sumar 1.
  Nunca reutilizar ni renumerar un ID existente, aunque se borre o mueva el escenario.
- **Scenario Outline:** cada fila es un caso con ID propio. Agregar la columna `case` (`01`, `02`…)
  como primera columna de `Examples` y nombrar el outline `QA_NNNN_<case> ...`
  (resultado: `QA_0002_01`, `QA_0002_02`…). Ejemplo: `features/QA0002_login_errors.feature`.
- **Feature nuevo:** archivo `features/QANNNN_<nombre>.feature`, con el ID de su escenario, y módulo
  pytest `tests/step_defs/test_qannnn_<nombre>.py` (en minúscula).
- Antes de escribir una frase nueva, buscar si ya existe un step que sirva:
  `grep -n "@given\|@when\|@then\|@step" features/steps/saucedemo_steps.py`.
  Reutilizar una frase existente evita implementar dos steps nuevos.
- Tag nuevo → registrarlo en `markers` de `pytest.ini` (si no, pytest lo reporta como desconocido).
- Si un valor de `Examples` puede venir vacío, la frase del step debe tolerarlo (ver punto 2 y 3).
- Las tablas de datos llevan **fila de encabezado**.
- Nunca escribir la contraseña de `settings.PASSWORD` en el feature: para entrar se usa
  `Given I am logged in as "<user>"`.

## 2. Implementar en behave

- Todo va en `features/steps/saucedemo_steps.py` (en behave los steps son globales).
- Valor que puede venir vacío: usar el tipo `{x:Text}` ya registrado.
- Step usado como Given y como When (Background + escenario): `@step` sirve para ambos.
- Page Objects disponibles en `context.login_page`, `context.inventory_page`, `context.cart_page`,
  `context.checkout_page`.
- Tablas: `context.table` (la fila 1 ya es el encabezado).

## 3. Implementar en pytest-bdd

- Step usado por un solo feature → `tests/step_defs/test_<feature>.py`.
- Step usado por dos o más features → `tests/conftest.py` (moverlo ahí apenas lo pida el segundo).
- **Feature nuevo** → crear `tests/step_defs/test_<feature>.py` con `scenarios("<feature>.feature")`.
  Sin este módulo, pytest no ejecuta el feature y no avisa.
- Valor que puede venir vacío: `parsers.re` con `(?P<x>[^"]*)`; `parsers.parse` con `{x}` exige
  al menos un carácter.
- Step usado como Given en un Background y como When en un escenario: apilar `@given` y `@when`
  sobre la misma función.
- Tablas: recibir `datatable` y saltar el encabezado con `datatable[1:]`.
- Page Objects llegan como fixtures: `login_page`, `inventory_page`, `cart_page`, `checkout_page`.

## 4. Page Objects (solo si hace falta una pantalla o acción nueva)

- Localizadores con `page.get_by_test_id("<valor de data-test>")`; CSS solo si el elemento no
  tiene `data-test`.
- Los Page Objects **no** llevan `expect` ni `assert`: las verificaciones van en los steps.
- Page Object nuevo → conectarlo en tres lugares:
  1. exportarlo en `pages/__init__.py`;
  2. crearlo en `before_scenario` de `features/environment.py`;
  3. agregar su fixture en `tests/conftest.py`.

## 5. Verificar

Ejecutar el escenario en los dos runners y después las dos suites completas:

```
.venv/Scripts/behave -n "<nombre del escenario>"
.venv/Scripts/python -m pytest -k "<nombre_en_snake_case>"
.venv/Scripts/behave
.venv/Scripts/python -m pytest
```

Ambas deben reportar el mismo número de escenarios y todos en verde. Si una suite tiene un
escenario más o menos que la otra, falta un `scenarios(...)` o un tag mal registrado.

## Lista de control final

- [ ] La frase es idéntica en el feature, en behave y en pytest-bdd.
- [ ] Tag nuevo registrado en `pytest.ini`.
- [ ] Feature nuevo con su `tests/step_defs/test_<feature>.py`.
- [ ] Page Object nuevo conectado en los tres lugares.
- [ ] Las dos suites en verde con el mismo número de escenarios.
