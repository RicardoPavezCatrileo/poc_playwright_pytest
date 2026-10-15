# POC Playwright + BDD — Sauce Demo

Pruebas E2E de [saucedemo.com](https://www.saucedemo.com) escritas en Gherkin (español) con Playwright (Python).
Los mismos `.feature` se pueden ejecutar con **behave** o con **pytest-bdd**.

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Ejecución con behave

```powershell
behave                                   # todo (headless, chromium)
behave --tags=smoke                      # por tag (@smoke, @login, @cart, ...)
behave features/login.feature            # una feature
behave -n "Compra completa"              # un escenario por nombre
behave -D headed=true -D slowmo=500      # ver el navegador
behave -D browser=firefox                # otro navegador (requiere playwright install firefox)
behave --format progress                 # salida compacta
```

Configuración por defecto en `behave.ini`. Ante una falla se guardan screenshot y trace en `test-results/behave/<escenario>/`.

## Ejecución con pytest-bdd

```powershell
pytest                                   # todo (headless, chromium)
pytest --headed --slowmo 500             # ver el navegador
pytest -m smoke                          # por tag de Gherkin (@smoke, @login, @cart, ...)
pytest tests/step_defs/test_login.py     # una feature
pytest -k "compra_completa"              # un escenario (nombre del escenario en snake_case)
pytest --browser firefox                 # otro navegador (requiere playwright install firefox)
```

Ante una falla se guardan screenshot y trace en `test-results/`. Para ver el trace:

```powershell
playwright show-trace test-results/<carpeta>/trace.zip
```

## Estructura

```
features/                 Archivos .feature (Gherkin en español, "# language: es") — compartidos
features/environment.py   [behave] hooks: abre/cierra Playwright, screenshot + trace al fallar
features/steps/           [behave] steps de todas las features
pages/                    Page Objects (localizadores + acciones) — compartidos
tests/conftest.py         [pytest-bdd] fixtures de Page Objects y steps compartidos
tests/step_defs/          [pytest-bdd] un test_*.py por feature: scenarios("x.feature") + steps propios
```

Los steps existen en dos implementaciones (behave y pytest-bdd) con las mismas frases: si se agrega o cambia un step en un `.feature`, hay que implementarlo en ambas.

## Cobertura

| Feature   | Escenarios |
|-----------|------------|
| login     | login exitoso, usuario bloqueado, credenciales inválidas, campos vacíos, logout |
| inventory | 6 productos visibles, ordenamiento por nombre y precio (4 variantes) |
| cart      | agregar varios productos, quitar producto |
| checkout  | compra completa con validación de total, campos obligatorios (3 variantes) |
