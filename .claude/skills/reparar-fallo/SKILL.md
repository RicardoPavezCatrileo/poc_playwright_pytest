---
name: reparar-fallo
description: Diagnosticar y reparar un escenario que falla o es inestable (flaky) en behave o pytest-bdd, distinguiendo si el problema es de la prueba o de la aplicación. Usar cuando un escenario esté en rojo, falle de forma intermitente o falle en un solo runner.
---

# Reparar un escenario que falla

Regla principal: **el `.feature` es el criterio de verdad.** Si la app no hace lo que el escenario
declara, el escenario debe seguir fallando. Nunca se ablanda ni se quita una aserción para dejarlo
en verde.

## 1. Reproducir antes de tocar código

```
.venv/Scripts/behave -n "<nombre del escenario>"
.venv/Scripts/python -m pytest -k "<nombre_en_snake_case>"
```

Ejecutar en **los dos runners**. Lo que muestre la comparación ya orienta el diagnóstico:

| Resultado | Causa más probable |
|---|---|
| Falla en los dos | Page Object, localizador, datos o un cambio real de la app |
| Falla solo en uno | La implementación del step difiere entre runners (parser, tipo de step, tabla) |
| A veces pasa y a veces falla | Inestabilidad: espera, estado compartido o datos |

Para ver la ejecución: `-D headed=true -D slowmo=500` (behave) o `--headed --slowmo 500` (pytest).

## 2. Revisar la evidencia

- Consola: step que falló, valor esperado y obtenido.
- Screenshot: `test-results/behave/<escenario>/screenshot.png` o `test-results/pytest/<test>/`.
- Trace: `.venv/Scripts/playwright show-trace <carpeta>/trace.zip` (DOM antes/después, red, acciones).

## 3. Clasificar la causa (una principal)

| Tipo | Señal | Dónde se corrige |
|---|---|---|
| **Step no encontrado** | `StepDefinitionNotFound` / `NotImplementedError` / "undefined step" | La frase no coincide entre el feature y el step → corregir el step en el runner que falla |
| **Parser** | Falla solo con un valor vacío de `Examples` | behave: `{x:Text}`; pytest-bdd: `parsers.re` con `[^"]*` |
| **Tipo de step** | Falla solo en pytest-bdd, step usado en Background y en escenario | Apilar `@given` y `@when` |
| **Selector** | Timeout esperando un elemento | `pages/`: revisar el `data-test` actual en el trace |
| **Timing** | Falla intermitente, aserción antes de que cargue la página | Usar `expect(...)` (espera sola); nunca `time.sleep()` ni `wait_for_timeout` |
| **Datos** | Producto, total o mensaje distinto al del feature | Confirmar en el trace si cambió la app o el dato de prueba |
| **Configuración** | `RuntimeError: Falta la variable ...` al importar | Completar `.env` desde `.env.example` |
| **Funcional** | La app no cumple lo que declara el feature | **No se repara.** Ver punto 5 |

## 4. Aplicar el cambio mínimo

- Corregir solo en la capa donde está la causa: `pages/`, los steps o la configuración.
- Si el cambio está en un step, aplicarlo en **los dos runners**
  (`features/steps/saucedemo_steps.py` y `tests/`).
- No cambiar el texto ni la intención del `.feature`, salvo que el usuario lo pida.
- Inestabilidad, en este orden: aserción con `expect` → esperar un estado visible concreto (no
  `networkidle`) → aislar estado entre escenarios. Reintentar no es una solución.
- Volver a ejecutar el escenario en los dos runners y después las dos suites completas.

## 5. Si el fallo es funcional

Dejar el escenario fallando e informar al usuario con:
- el escenario y el step que falla;
- el valor esperado (del feature) y el obtenido (de la app);
- la ruta del screenshot y del trace.

La decisión de reportarlo como defecto o de cambiar el feature es del usuario.

## Si falta información

Si no se puede reproducir o la evidencia no alcanza para clasificar la causa, detenerse y explicar
qué falta, en vez de aplicar un cambio a ciegas.
