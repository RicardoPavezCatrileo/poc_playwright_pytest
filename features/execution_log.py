"""Log de ejecución por caso de prueba (behave).

Un archivo por caso y por día: test-results/logs/<YYYYMMDD>/<NB>_<QA_ID>_<YYYYMMDD>.log
Si el mismo caso se ejecuta varias veces en el día, las ejecuciones se agregan al mismo archivo.
"""
import logging
import re
import time
from datetime import datetime
from pathlib import Path

LOGS_DIR = Path(__file__).resolve().parent.parent / "test-results" / "logs"
LINE = "=" * 80

# Logger propio sin propagar: behave captura el logger raíz y lo mostraría en consola
logger = logging.getLogger("saucedemo")
logger.setLevel(logging.INFO)
logger.propagate = False


def _qa_id(scenario):
    match = re.match(r"(QA_\d+(?:_\d+)?)", scenario.name)
    return match.group(1) if match else "SIN_ID"


def start_scenario(context, scenario):
    """Abre el archivo de log del caso y escribe el bloque [Setup]."""
    now = datetime.now()
    userdata = context.config.userdata
    browser = userdata.get("browser", "chromium").upper()
    nb = f"POC_SAUCEDEMO_{browser}"
    qa_id = _qa_id(scenario)

    log_path = LOGS_DIR / now.strftime("%Y%m%d") / f"{nb}_{qa_id}_{now:%Y%m%d}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handler = logging.FileHandler(log_path, mode="a", encoding="utf-8")
    handler.setFormatter(logging.Formatter(f"%(asctime)s - [NB: {nb}] - %(levelname)s - %(message)s"))
    logger.addHandler(handler)

    context.log_handler = handler
    context.log_start = time.perf_counter()
    context.log_steps = list(scenario.all_steps)
    context.log_step_index = 0

    tags = " ".join(f"@{t}" for t in scenario.effective_tags)
    logger.info(LINE)
    logger.info(f"[Setup] Ejecución  : {nb}_{qa_id}_{now:%Y%m%d-%H%M%S}")
    logger.info(f"Inicia la ejecución SCENARIO: {scenario.name}")
    logger.info(LINE)
    logger.info(f"[Setup] Feature    : {Path(scenario.feature.filename).name}")
    logger.info(f"[Setup] QA Case    : {qa_id}")
    logger.info(f"[Setup] Tags       : {tags}")
    logger.info(f"[Setup] Ambiente   : {context.base_url} | Browser: {browser}"
                f" | Headless: {not userdata.getbool('headed', False)}")
    logger.info(f"[Setup] Log        : {log_path.relative_to(LOGS_DIR.parent.parent)}")
    logger.info(LINE)


def start_step(context, step):
    context.log_step_index += 1
    total = len(context.log_steps)
    logger.info(f"[STEP {context.log_step_index}/{total}] {step.keyword} {step.name}")


def end_step(context, step):
    total = len(context.log_steps)
    status = step.status.name.upper()
    msg = f"[STEP {context.log_step_index}/{total}] {status} ({step.duration:.2f}s)"
    if status == "PASSED":
        logger.info(msg)
    else:
        logger.error(msg)
        if step.error_message:
            for line in step.error_message.strip().splitlines():
                logger.error(f"    {line}")


def finish_scenario(context, scenario, evidence=None):
    """Escribe el cierre (estado, duración y tabla de steps) y cierra el archivo."""
    statuses = [s.status.name for s in context.log_steps]
    total = len(statuses)
    passed = statuses.count("passed")
    failed = statuses.count("failed") + statuses.count("error")
    not_completed = total - passed - failed
    state = scenario.status.name.upper()

    if evidence:
        logger.warning(f"📸 Screenshot: {evidence / 'screenshot.png'}")
        logger.warning(f"🔍 Trace     : playwright show-trace {evidence / 'trace.zip'}")

    logger.info(LINE)
    logger.info("PRUEBA FINALIZADA")
    logger.info(f"Hora de finalizacion : {datetime.now():%Y-%m-%d %H:%M:%S}")
    logger.info(f"Escenario            : {scenario.name}")
    logger.info(f"Estado               : {state}")
    logger.info(f"Duracion             : {time.perf_counter() - context.log_start:.1f}s")
    logger.info(LINE)

    def pct(n):
        return f"{round(n * 100 / total) if total else 0}%"

    def row(text):
        return f"   | / | {text:<45} | \\ |"

    for line in [
        "   __^__" + " " * 47 + "__^__",
        "  ( ___ )" + "-" * 45 + "( ___ )",
        row(f"{'Steps':^45}"),
        row(f"{'Estado':^13} | {'Cantidad':^10} | {'Porcentaje(%)':^16}"),
        row(f"{'PASSED':^13} | {passed:<10} | {pct(passed):<16}"),
        row(f"{'FAILED':^13} | {failed:<10} | {pct(failed):<16}"),
        row(f"{'NOT COMPLETED':^13} | {not_completed:<10} | {pct(not_completed):<16}"),
        row(""),
        row(f"Total Steps = {total}"),
        row(f"Caso QA     = {_qa_id(scenario)}"),
        "   |___|" + " " * 47 + "|___|",
        "  (_____)" + "-" * 45 + "(_____)",
    ]:
        (logger.info if state == "PASSED" else logger.error)(line)

    logger.removeHandler(context.log_handler)
    context.log_handler.close()
