# POC Playwright + pytest-bdd — Sauce Demo

Pruebas E2E de [saucedemo.com](https://www.saucedemo.com) escritas en Gherkin (español) y ejecutadas con pytest-bdd y Playwright (Python).

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
```

## Ejecución

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
features/          Archivos .feature (Gherkin en español, "# language: es")
pages/             Page Objects (localizadores + acciones)
tests/conftest.py  Fixtures de Page Objects y steps compartidos entre features
tests/step_defs/   Un test_*.py por feature: scenarios("x.feature") + steps propios
```

## Cobertura

| Feature   | Escenarios |
|-----------|------------|
| login     | login exitoso, usuario bloqueado, credenciales inválidas, campos vacíos, logout |
| inventory | 6 productos visibles, ordenamiento por nombre y precio (4 variantes) |
| cart      | agregar varios productos, quitar producto |
| checkout  | compra completa con validación de total, campos obligatorios (3 variantes) |
