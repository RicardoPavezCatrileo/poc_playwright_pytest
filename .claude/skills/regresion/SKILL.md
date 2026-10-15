---
name: regresion
description: Ejecutar la regresión completa o el smoke en los dos runners (behave y pytest-bdd), comparar resultados, clasificar fallos y emitir una decisión GO / CAUTION / NO-GO. Usar antes de un commit importante, al pedir "correr todo", "regresión", "smoke" o "estado de las pruebas".
---

# Regresión en los dos runners

Fases obligatorias, en orden: **Ejecutar → Analizar → Reportar.** No se emite decisión sin haber
ejecutado.

## 1. Ejecutar

Completa (por defecto):

```
.venv/Scripts/behave --format progress
.venv/Scripts/python -m pytest -q -rf
```

Solo smoke (camino crítico, un escenario por feature):

```
.venv/Scripts/behave --tags=smoke --format progress
.venv/Scripts/python -m pytest -m smoke -q -rf
```

Si falta el `.env`, la ejecución se detiene al importar `settings.py`: eso es un problema de
entorno, no un resultado.

## 2. Analizar

Primero comparar los totales: **las dos suites deben ejecutar el mismo número de escenarios.**
Si no coinciden, falta un `scenarios(...)` en `tests/step_defs/` o un tag no registrado en
`pytest.ini`.

Para cada escenario fallido, volver a ejecutarlo solo una vez en el runner donde falló y
clasificarlo:

| Clase | Criterio |
|---|---|
| **REGRESIÓN** | Falla en los dos runners de forma consistente y antes pasaba |
| **DIVERGENCIA** | Falla en un solo runner: los steps de behave y pytest-bdd no hacen lo mismo |
| **FLAKY** | Falla y al repetirlo pasa |
| **ENTORNO** | Sitio caído, red, `.env` incompleto, navegador no instalado |
| **NUEVO** | Escenario recién agregado que nunca pasó |

Para diagnosticar la causa de cada uno, usar la skill `reparar-fallo`. Esta skill solo clasifica
y decide; no modifica código.

## 3. Decidir

- **GO:** las dos suites en verde, con el mismo número de escenarios.
- **CAUTION:** solo fallos FLAKY o ENTORNO fuera de `@smoke`, con la causa identificada.
- **NO-GO:** cualquier fallo en un escenario `@smoke`, cualquier REGRESIÓN o DIVERGENCIA,
  totales distintos entre runners, o evidencia insuficiente.

## 4. Reportar

Formato de salida:

1. **Decisión** (GO / CAUTION / NO-GO) en la primera línea, con el motivo en una frase.
2. Tabla de métricas:

   | Runner | Escenarios | Pasaron | Fallaron | Omitidos | Duración |
   |---|---|---|---|---|---|

3. Fallos clasificados: escenario, runner, clase, evidencia (`test-results/...`) y acción
   propuesta (reparar, reintentar, revisar con el usuario).
4. Siguiente paso recomendado.
