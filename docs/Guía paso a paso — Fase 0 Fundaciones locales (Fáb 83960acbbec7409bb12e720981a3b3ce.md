# Guía paso a paso — Fase 0: Fundaciones locales (Fábrica de Desarrollo con Agentes IA)

Categoría: Proyectos
Fecha: 3 de agosto de 2026
Etiquetas: Código, Importante, Proyecto
ítem principal: Plan de Implementación — Fábrica de Desarrollo con Agentes IA (local / validación de grafo) (https://app.notion.com/p/Plan-de-Implementaci-n-F-brica-de-Desarrollo-con-Agentes-IA-local-validaci-n-de-grafo-3878229d6b0d48c28e5590c8f65c6c56?pvs=21)

<aside>
🧩

**Qué es este documento.** Guía de ejecución paso a paso, pensada para principiantes, del plan [Plan de Implementación — Fábrica de Desarrollo con Agentes IA (local / validación de grafo)](https://app.notion.com/p/Plan-de-Implementaci-n-F-brica-de-Desarrollo-con-Agentes-IA-local-validaci-n-de-grafo-3878229d6b0d48c28e5590c8f65c6c56?pvs=21). Cubre con el máximo detalle la **Fase 0 — Fundaciones locales** (§12 del plan): todos los comandos y todo el código, en el orden exacto en que se ejecutan en tu máquina. Al final se incluye, a modo de hoja de ruta, un resumen de las Fases 1 a 5, que se detallarán con este mismo nivel de profundidad cuando llegue el momento de ejecutarlas.

</aside>

<aside>
💻

**Nota sobre Windows.** Todos los comandos de esta guía están escritos para una terminal tipo Mac/Linux (bash). Si usas Windows, instala **WSL2** cuando Docker Desktop te lo pida durante la instalación (paso 1) y ejecuta todos los comandos de esta guía dentro de una terminal de **Ubuntu (WSL2)** en lugar de PowerShell: así los comandos son idénticos, letra por letra, a los de esta guía.

</aside>

## 0. Antes de empezar

Revisa que tengas esto listo antes de escribir el primer comando:

- [x]  Una cuenta de GitHub con acceso a la organización **ADN Fábrica Lab**. Si no la tienes, pídele acceso a Andrés antes de seguir.
- [x]  Un **token de OpenRouter** (pídeselo a Andrés si no lo tienes).
- [x]  Permisos de administrador en tu computador para instalar programas.
- [x]  Conexión a internet estable (vas a descargar programas de varios cientos de MB).

### 0.1 Programas que vas a instalar

| Programa | Para qué sirve | Dónde descargarlo |
| --- | --- | --- |
| Docker Desktop | Corre todos los contenedores (Postgres, Qdrant, el orquestador, el sandbox) sin instalar nada directo en tu sistema | [docker.com/products/docker-desktop](http://docker.com/products/docker-desktop) |
| Git | Para clonar y trabajar con repositorios de GitHub | [git-scm.com/downloads](http://git-scm.com/downloads) |
| Visual Studio Code (opcional, recomendado) | Editor para ver y modificar los archivos que vamos a crear | [code.visualstudio.com](http://code.visualstudio.com) |

## 1. Instalar Docker Desktop

1. Entra a [**docker.com/products/docker-desktop**](http://docker.com/products/docker-desktop) y descarga la versión para tu sistema (Windows, Mac Apple Silicon, Mac Intel, o Linux).
2. Instala el programa como cualquier otro: doble clic al instalador y sigue los pasos. En Windows, si te pide activar **WSL2**, acepta — es un requisito de Docker en Windows.
3. Abre Docker Desktop y espera a que el ícono de la ballena 🐳 indique **"Running"**. La primera vez puede tardar 1–2 minutos.
4. Abre una terminal y verifica la instalación:

```bash
docker --version
docker compose version
```

Deberías ver algo como `Docker version 27.x.x` y `Docker Compose version v2.x.x`. Si sale "command not found", cierra y vuelve a abrir la terminal, o reinicia el computador.

## 2. Instalar Git

1. Ve a [**git-scm.com/downloads**](http://git-scm.com/downloads) y descarga para tu sistema.
2. Instala dejando las opciones por defecto.
3. Verifica:

```bash
git --version
```

## 3. Crear la carpeta del proyecto

Elige dónde guardar el proyecto (por ejemplo tu carpeta de Documentos) y desde la terminal:

```bash
cd ~/Documents
mkdir fabrica-desarrollo-ia
cd fabrica-desarrollo-ia
```

Vamos a construir esta estructura de archivos a lo largo de la guía:

```
fabrica-desarrollo-ia/
├── docker-compose.yml
├── .env
├── .gitignore
├── orquestador/
│   ├── Dockerfile
│   ├── requirements.txt
│   └── src/
│       ├── state.py
│       ├── graph.py
│       └── main.py
└── sandbox/
    └── Dockerfile
```

Crea ya las carpetas:

```bash
mkdir -p orquestador/src
mkdir -p sandbox
```

## 4. Crear el archivo `.env` (tokens y contraseñas)

Este archivo guarda información sensible; **nunca se sube a GitHub**.

```bash
touch .env .gitignore
echo ".env" >> .gitignore
```

Abre `.env` en tu editor y pega esto, reemplazando el valor de `OPENROUTER_API_KEY` por el token real que te dé Andrés:

```
# --- OpenRouter ---
OPENROUTER_API_KEY=pega_aqui_el_token_que_te_da_andres

# --- Postgres (estado y checkpoints del grafo) ---
POSTGRES_USER=fabrica
POSTGRES_PASSWORD=cambia_esta_clave
POSTGRES_DB=fabrica_desarrollo
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# --- Qdrant (RAG) ---
QDRANT_HOST=qdrant
QDRANT_PORT=6333

# --- GitHub (se completa en el paso 14) ---
GITHUB_TOKEN=
GITHUB_ORG=adn-fabrica-lab
```

## 5. Crear `docker-compose.yml`

En la raíz del proyecto, crea el archivo `docker-compose.yml` con este contenido exacto:

```yaml
services:
  postgres:
    image: postgres:16
    container_name: fabrica_postgres
    restart: unless-stopped
    env_file: .env
    environment:
      POSTGRES_USER: ${POSTGRES_USER}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      POSTGRES_DB: ${POSTGRES_DB}
    ports:
      - "5432:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data

  qdrant:
    image: qdrant/qdrant:latest
    container_name: fabrica_qdrant
    restart: unless-stopped
    ports:
      - "6333:6333"
    volumes:
      - qdrant_data:/qdrant/storage

  orquestador:
    build: ./orquestador
    container_name: fabrica_orquestador
    restart: unless-stopped
    env_file: .env
    depends_on:
      - postgres
      - qdrant
    volumes:
      - ./orquestador/src:/app/src
    stdin_open: true   # necesario para los checkpoints humanos por terminal (§10 del plan)
    tty: true

  sandbox:
    build: ./sandbox
    container_name: fabrica_sandbox
    restart: unless-stopped
    volumes:
      - sandbox_workspace:/workspace

volumes:
  postgres_data:
  qdrant_data:
  sandbox_workspace:
```

Cada servicio corresponde a una pieza de la arquitectura del plan (§8): `postgres` guarda el estado y los checkpoints del grafo, `qdrant` es el RAG, `orquestador` es el grafo de LangGraph, y `sandbox` es el entorno aislado donde luego correrá el código generado (NestJS/Next.js).

## 6. Crear el `Dockerfile` del orquestador

Crea el archivo `orquestador/Dockerfile`:

```docker
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY src ./src

CMD ["python", "src/main.py"]
```

## 7. Crear `requirements.txt`

Crea el archivo `orquestador/requirements.txt`:

```
langgraph>=0.2.0
langgraph-checkpoint-postgres>=2.0.0
langchain-openai>=0.2.0
psycopg[binary]>=3.1.0
python-dotenv>=1.0.0
```

**Por qué estas librerías:** `langgraph` es el motor del grafo; `langgraph-checkpoint-postgres` conecta el grafo a Postgres para los checkpoints (§10); `langchain-openai` se usa para hablar con OpenRouter (es compatible con la API de OpenAI); `psycopg` es el driver de Postgres; `python-dotenv` carga el archivo `.env`.

## 8. Crear el `Dockerfile` del sandbox

Crea el archivo `sandbox/Dockerfile` (entorno donde correrá el código NestJS/Next.js generado por los agentes, a partir de la Fase 1):

```docker
FROM node:20-bookworm

WORKDIR /workspace

RUN npm install -g @nestjs/cli

CMD ["sleep", "infinity"]
```

Este contenedor queda "vivo pero en espera"; en fases siguientes se usará `docker compose exec sandbox ...` para correr y probar el código que escriban los agentes.

## 9. Ubicar y copiar el código base de la Fábrica de Encargos (§4.2)

El plan confirma que este piloto **no arranca en blanco**: se reutiliza el código del grafo de LangGraph y de los agentes ya construido para la Fábrica de Encargos. Antes de escribir código nuevo:

1. Pídele a Andrés (o a quien tenga acceso) la **ubicación del repositorio** de código de la Fábrica de Encargos.
2. Clónalo en una carpeta separada, solo como referencia (fuera de `fabrica-desarrollo-ia`):

```bash
cd ~/Documents
git clone <url-del-repo-fabrica-encargos> fabrica-encargos-referencia
```

1. Dentro de ese repositorio, ubica (pide ayuda a quien lo conozca si hace falta) los archivos equivalentes a:
    - El **esqueleto del `StateGraph`** (suele llamarse `graph.py`, `workflow.py` o similar).
    - La **conexión al checkpointer de Postgres**.
    - La **capa de abstracción de modelos sobre OpenRouter** (por ejemplo `models.py` o `llm.py`).
2. Copia esos archivos (o su lógica) como punto de partida dentro de `orquestador/src/` de este nuevo proyecto. En el paso 10 los adaptamos al estado nuevo de esta fábrica (§4.1); no son una copia final.

<aside>
⚠️

Si todavía no tienes acceso a ese repositorio o nadie puede mostrártelo a tiempo, puedes seguir con el paso 10 usando el esqueleto genérico que se te da ahí (parte de cero en el checkpointer y la conexión a Postgres, sin la capa de abstracción de OpenRouter de Encargos) y reemplazarlo por el código real de Encargos apenas lo tengas, sin perder avance.

</aside>

## 10. Escribir el esqueleto del grafo (`state.py`, `graph.py`, `main.py`)

Crea `orquestador/src/state.py` con el estado definido en §4.1 del plan:

```python
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
    rama_git: str
    aprobacion_final: bool
    ciclo: int
    trazas: list[str]
```

Crea `orquestador/src/graph.py` con el esqueleto del `StateGraph` conectado al checkpointer de Postgres (en esta fase el único nodo es un placeholder; los nodos reales del catálogo de agentes de §5 se implementan en la Fase 1):

```python
# orquestador/src/graph.py
import os

from langgraph.graph import StateGraph, END
from langgraph.checkpoint.postgres import PostgresSaver

from state import EstadoFabricaDesarrollo

def _nodo_coordinador(estado: EstadoFabricaDesarrollo) -> EstadoFabricaDesarrollo:
    # Placeholder de Fase 0: en la Fase 1 este nodo interpreta el encargo real (§5).
    print("Coordinador: recibiendo encargo...", estado.get("encargo_id"))
    return estado

def construir_grafo():
    builder = StateGraph(EstadoFabricaDesarrollo)
    builder.add_node("coordinador", _nodo_coordinador)
    builder.set_entry_point("coordinador")
    builder.add_edge("coordinador", END)

    db_uri = (
        f"postgresql://{os.environ['POSTGRES_USER']}:{os.environ['POSTGRES_PASSWORD']}"
        f"@{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/{os.environ['POSTGRES_DB']}"
    )
    checkpointer = PostgresSaver.from_conn_string(db_uri)
    checkpointer.setup()  # crea las tablas de checkpoint la primera vez que corre

    return builder.compile(checkpointer=checkpointer)
```

Crea `orquestador/src/main.py`, el punto de entrada que usaremos para probar que todo funciona:

```python
# orquestador/src/main.py
from dotenv import load_dotenv

from graph import construir_grafo

load_dotenv()

if __name__ == "__main__":
    grafo = construir_grafo()
    resultado = grafo.invoke(
        {"encargo_id": "prueba-001", "ciclo": 0},
        config={"configurable": {"thread_id": "prueba-001"}},
    )
    print("Resultado:", resultado)
```

## 11. Levantar todo con Docker

Desde la raíz del proyecto (`fabrica-desarrollo-ia/`):

```bash
docker compose up -d --build
```

- `--build` reconstruye las imágenes de `orquestador` y `sandbox` a partir de sus Dockerfiles.
- `-d` corre los contenedores en segundo plano ("detached").

La primera vez puede tardar varios minutos (descarga imágenes de Postgres, Qdrant, Python y Node). Verifica que todo quedó arriba:

```bash
docker compose ps
```

Deberías ver 4 servicios (`postgres`, `qdrant`, `orquestador`, `sandbox`) en estado `Up`. Si alguno no queda "Up", revisa su log:

```bash
docker compose logs orquestador
```

## 12. Probar que el esqueleto del grafo corre

```bash
docker compose exec orquestador python src/main.py
```

Deberías ver algo como:

```
Coordinador: recibiendo encargo... prueba-001
Resultado: {'encargo_id': 'prueba-001', 'ciclo': 0}
```

Si ves un error de conexión a Postgres, espera unos segundos (Postgres tarda un poco en arrancar la primera vez) y vuelve a correr el comando.

## 13. Verificar Postgres y Qdrant

**Postgres** — confirma que el checkpointer creó sus tablas:

```bash
docker compose exec postgres psql -U fabrica -d fabrica_desarrollo -c "\dt"
```

Deberías ver tablas cuyo nombre empieza con `checkpoint`.

**Qdrant** — confirma que responde:

```bash
curl http://localhost:6333/collections
```

Deberías ver algo como `{"result":{"collections":[]},"status":"ok",...}`.

## 14. Confirmar acceso a GitHub — ADN Fábrica Lab

1. Entra a la página de la organización **ADN Fábrica Lab** en GitHub y confirma que puedes ver sus repositorios. Si no tienes acceso, pídele a Andrés que te invite.
2. Genera un **Personal Access Token**: en GitHub ve a `Settings → Developer settings → Personal access tokens → Generate new token`, con permisos de `repo`.
3. Copia ese token y pégalo en tu `.env`:

```
GITHUB_TOKEN=el_token_que_generaste
```

1. Prueba que el token funciona clonando cualquier repo de prueba de la organización:

```bash
git clone https://<tu-usuario>:<GITHUB_TOKEN>@github.com/<org>/<repo-de-prueba>.git
```

## 15. Checklist final de la Fase 0

- [x]  Docker Desktop instalado y corriendo
- [x]  Git instalado
- [x]  Carpeta `fabrica-desarrollo-ia` creada con toda la estructura de archivos
- [x]  `.env` completo (OpenRouter, Postgres, GitHub) y agregado a `.gitignore`
- [x]  `docker-compose.yml` y los `Dockerfile` de `orquestador` y `sandbox` creados
- [x]  Código base de la Fábrica de Encargos ubicado y copiado como punto de partida (§4.2), o marcado como pendiente si aún no hay acceso
- [x]  `state.py`, `graph.py` y `main.py` creados con el esqueleto de `StateGraph` y el checkpointer de Postgres
- [x]  `docker compose up -d --build` corre sin errores y los 4 contenedores están "Up"
- [x]  `docker compose exec orquestador python src/main.py` corre y muestra el resultado del grafo
- [x]  Postgres muestra las tablas `checkpoint*` creadas
- [x]  Qdrant responde en `http://localhost:6333/collections`
- [x]  Acceso confirmado a GitHub ADN Fábrica Lab y token generado

<aside>
✅

Cuando completes esta checklist, la Fase 0 está lista. El siguiente paso es la **Fase 1 — Grafo mínimo** (§12 del plan): pide que se detalle con este mismo nivel de paso a paso cuando estés listo para empezarla.

</aside>

## 16. Hoja de ruta — Fases 1 a 5 (resumen)

Estas fases se detallarán con el mismo nivel de profundidad (comandos y código completos) más adelante, cuando corresponda ejecutarlas. Por ahora, este es el resumen de qué implica cada una según el plan (§12):

| Fase | Qué se hace |
| --- | --- |
| Fase 1 — Grafo mínimo | Implementar Coordinador, Arquitecto y un solo programador (Backend); probar de punta a punta con un encargo pequeño |
| Fase 2 — Frontend y afinar el grafo | Sumar el Programador Frontend, confirmar el Integrador, afinar el Revisor de Código |
| Fase 3 — Estrategia de código y RAG | Validar "working copy + rama por encargo" con un proyecto de varios archivos; cargar el RAG con documentación de NestJS/Next.js |
| Fase 4 — Checkpoints e intervención humana | Implementar los checkpoints por terminal y el ciclo de corrección (humano rechaza → vuelve al agente correspondiente) |
| Fase 5 — Validación del grafo | Correr 2–3 encargos representativos y documentar el grafo final afinado como insumo para producción |