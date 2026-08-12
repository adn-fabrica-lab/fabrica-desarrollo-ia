# orquestador/src/rag.py
import os

from qdrant_client import QdrantClient

COLECCION_POR_AREA = {
    "backend": "docs_nestjs",
    "frontend": "docs_nextjs",
    "db": "docs_prisma",
}

_cliente = None


def _obtener_cliente() -> QdrantClient:
    global _cliente
    if _cliente is None:
        _cliente = QdrantClient(
            host=os.environ.get("QDRANT_HOST", "qdrant"),
            port=int(os.environ.get("QDRANT_PORT", "6333")),
        )
    return _cliente


def consultar_rag(consulta: str, area: str, limite: int = 3) -> list[str]:
    """Devuelve fragmentos de documentacion oficial y skills relevantes.

    area: "backend" (NestJS), "frontend" (Next.js), "db" (Prisma) o "ambas".
    Si la coleccion no existe o Qdrant no responde, devuelve una lista vacia:
    el grafo sigue funcionando igual que en la Fase 2, solo sin contexto extra.
    """
    if area == "ambas":
        colecciones = list(COLECCION_POR_AREA.values())
    else:
        colecciones = [COLECCION_POR_AREA[area]]
    fragmentos = []
    for coleccion in colecciones:
        try:
            resultados = _obtener_cliente().query(
                collection_name=coleccion,
                query_text=consulta,
                limit=limite,
            )
        except Exception:
            continue
        for r in resultados:
            if r.document:
                fragmentos.append(r.document[:1200])
    return fragmentos
