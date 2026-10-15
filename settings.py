"""Configuración del proyecto leída desde .env (plantilla en .env.example).

Las variables de entorno reales tienen prioridad sobre el .env, así en CI
se pueden inyectar como secrets sin crear el archivo.
"""
import os
from pathlib import Path

from dotenv import load_dotenv

load_dotenv(Path(__file__).resolve().parent / ".env")


def _required(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Falta la variable {name}: copia .env.example a .env y complétala")
    return value


BASE_URL = _required("SAUCE_BASE_URL")
PASSWORD = _required("SAUCE_PASSWORD")
