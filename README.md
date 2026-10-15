# POC Playwright + BDD — Sauce Demo

Pruebas E2E de [saucedemo.com](https://www.saucedemo.com) escritas en Gherkin (inglés) con Playwright (Python).
Los mismos `.feature` se pueden ejecutar con **behave** o con **pytest-bdd**.

## Instalación

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
playwright install chromium
copy .env.example .env      # y completar SAUCE_PASSWORD
```

## Configuración (.env)

La URL del sitio y la contraseña se leen del archivo `.env` (vía `settings.py`), que **no se sube al repo** (está en `.gitignore`). `.env.example` es la plantilla con los nombres de las variables:

| Variable | Uso |
|---|---|
| `SAUCE_BASE_URL` | URL base del sitio (los Page Objects navegan con rutas relativas, ej. `/`) |
| `SAUCE_PASSWORD` | contraseña para los steps `I am logged in as "<usuario>"` |

Las variables de entorno del sistema tienen prioridad sobre el `.env` (útil en CI con secrets). La URL también se puede cambiar por ejecución con `pytest --base-url <url>` o `behave -D base_url=<url>`.

## Ejecución con behave

```powershell
behave                                   # todo (headless, chromium)
behave --tags=smoke                      # por tag (@smoke, @login, @cart, ...)
behave features/login.feature            # una feature
behave -n "Complete purchase"            # un escenario por nombre
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
pytest -k "complete_purchase"            # un escenario (nombre del escenario en snake_case)
pytest --browser firefox                 # otro navegador (requiere playwright install firefox)
```

Ante una falla se guardan screenshot y trace en `test-results/`. Para ver el trace:

```powershell
playwright show-trace test-results/<carpeta>/trace.zip
```

## Estructura

```
features/                 Archivos .feature (Gherkin en inglés) — compartidos
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

## VS Code

Al abrir la carpeta, VS Code sugiere instalar las extensiones recomendadas (`.vscode/extensions.json`):
**Cucumber** (oficial: ícono, colores y autocompletado en los `.feature`, Ctrl+clic para ir al step) y **Python**.
`.vscode/settings.json` apunta el intérprete al `.venv` y le indica a Cucumber dónde están los features y los steps de behave.
