# orquestador/src/skills.py
"""Busca y descarga skills desde skills.sh para enriquecer el RAG.

Uso tipico (desde cargar_rag.py):
    from skills import obtener_skills_para_area
    skills_backend = obtener_skills_para_area("backend", top_n=3)
"""
import json
import urllib.error
import urllib.parse
import urllib.request

# Queries de busqueda asociadas a cada area de la fabrica.
SKILLS_POR_AREA = {
    "backend": ["nestjs"],
    "frontend": ["nextjs", "tailwindcss", "shadcn"],
    "db": ["prisma"],
}


def buscar_skills(query: str, limit: int = 3) -> list[dict]:
    """Busca skills en skills.sh por palabra clave."""
    url = f"https://skills.sh/api/search?q={urllib.parse.quote(query)}&limit={limit}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    return data.get("skills") or []


def descargar_skill(skill_id: str) -> str:
    """Descarga el skill desde skills.sh usando el endpoint /api/download.

    El skill_id tiene la forma owner/repo/skillId. La respuesta JSON trae
    una lista de archivos (path, contents); concatenamos todos los contenidos.
    """
    partes = skill_id.split("/")
    if len(partes) < 3:
        raise ValueError(f"skill_id invalido: {skill_id}")
    owner, repo = partes[0], partes[1]
    slug = "/".join(partes[2:])
    url = f"https://skills.sh/api/download/{owner}/{repo}/{slug}"
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = json.loads(resp.read().decode("utf-8"))
    archivos = data.get("files") or []
    if not archivos:
        raise RuntimeError(f"El skill {skill_id} no devolvio archivos")
    contenidos = []
    for archivo in archivos:
        path = archivo.get("path", "")
        contents = archivo.get("contents", "")
        contenidos.append(f"--- {path} ---\n{contents}")
    return "\n\n".join(contenidos)


def obtener_skills_para_area(area: str, top_n: int = 3) -> list[dict]:
    """Devuelve skills descargadas para un area."""
    skills = []
    vistos = set()
    for query in SKILLS_POR_AREA.get(area, []):
        for resultado in buscar_skills(query, limit=top_n):
            skill_id = resultado.get("id")
            if not skill_id or skill_id in vistos:
                continue
            vistos.add(skill_id)
            try:
                contenido = descargar_skill(skill_id)
            except Exception as e:
                print(f"   Omitiendo skill {skill_id}: {e}")
                continue
            skills.append({
                "id": skill_id,
                "name": resultado.get("name", ""),
                "description": resultado.get("description", ""),
                "contenido": contenido,
            })
    return skills
