# orquestador/src/cargar_rag.py
"""Carga la documentacion publica de NestJS y Next.js en Qdrant (S7 del plan).

Uso (desde la raiz del proyecto):
    docker compose exec orquestador python src/cargar_rag.py          # ambas
    docker compose exec orquestador python src/cargar_rag.py nestjs   # solo una
Idempotente: cada corrida borra y recrea la coleccion correspondiente.
"""
import os
import subprocess
import sys
import tempfile

from qdrant_client import QdrantClient

FUENTES = {
    "nestjs": {
        "coleccion": "docs_nestjs",
        "repo": "https://github.com/nestjs/docs.nestjs.com.git",
        "carpeta_docs": "content",
        "extensiones": (".md",),
    },
    "nextjs": {
        "coleccion": "docs_nextjs",
        "repo": "https://github.com/vercel/next.js.git",
        "carpeta_docs": "docs",
        "extensiones": (".md", ".mdx"),
    },
}

TAMANO_FRAGMENTO = 1500
SOLAPAMIENTO = 200


def fragmentar(texto: str) -> list[str]:
    fragmentos = []
    inicio = 0
    while inicio < len(texto):
        fragmentos.append(texto[inicio : inicio + TAMANO_FRAGMENTO])
        inicio += TAMANO_FRAGMENTO - SOLAPAMIENTO
    return [f for f in fragmentos if len(f.strip()) > 100]


def descargar_docs(fuente: dict, destino: str) -> str:
    # Clone superficial y disperso: descarga solo la carpeta de documentacion,
    # no todo el repositorio (el monorepo de Next.js pesa cientos de MB).
    subprocess.run(
        ["git", "clone", "--depth", "1", "--filter=blob:none", "--sparse",
         fuente["repo"], destino],
        check=True,
    )
    subprocess.run(
        ["git", "-C", destino, "sparse-checkout", "set", fuente["carpeta_docs"]],
        check=True,
    )
    return os.path.join(destino, fuente["carpeta_docs"])


def cargar_fuente(cliente: QdrantClient, nombre: str) -> None:
    fuente = FUENTES[nombre]
    print("Descargando documentacion de " + nombre + "...")
    documentos, metadatos = [], []
    with tempfile.TemporaryDirectory() as tmp:
        raiz = descargar_docs(fuente, tmp)
        for carpeta, _, archivos in os.walk(raiz):
            for archivo in archivos:
                if not archivo.endswith(fuente["extensiones"]):
                    continue
                ruta = os.path.join(carpeta, archivo)
                with open(ruta, "r", encoding="utf-8", errors="ignore") as f:
                    texto = f.read()
                relativa = os.path.relpath(ruta, raiz)
                for fragmento in fragmentar(texto):
                    documentos.append(fragmento)
                    metadatos.append({"fuente": nombre, "archivo": relativa})
    print("   " + str(len(documentos)) + " fragmentos extraidos.")
    if cliente.collection_exists(fuente["coleccion"]):
        cliente.delete_collection(fuente["coleccion"])
    print("   Generando embeddings y cargando en Qdrant (varios minutos)...")
    cliente.add(
        collection_name=fuente["coleccion"],
        documents=documentos,
        metadata=metadatos,
    )
    print("   Coleccion " + fuente["coleccion"] + " lista.")


if __name__ == "__main__":
    objetivo = sys.argv[1] if len(sys.argv) > 1 else "todo"
    cliente = QdrantClient(
        host=os.environ.get("QDRANT_HOST", "qdrant"),
        port=int(os.environ.get("QDRANT_PORT", "6333")),
    )
    for nombre in FUENTES:
        if objetivo in ("todo", nombre):
            cargar_fuente(cliente, nombre)
    print("Carga de RAG terminada.")
