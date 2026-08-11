# orquestador/src/state.py
from typing import TypedDict


class EstadoFabricaDesarrollo(TypedDict):
    encargo_id: str
    encargo: dict
    plan_tecnico: dict
    plan_aprobado: bool
    archivos_backend: list[dict]
    archivos_frontend: list[dict]
    hallazgos_revision: list[dict]
    hallazgos_integracion: list[dict]
    resultado_sandbox: dict
    rama_git: str
    aprobacion_final: bool
    ciclo: int
    trazas: list[str]
    comentarios_humanos: str  # NUEVO Fase 4: comentarios del humano al rechazar
