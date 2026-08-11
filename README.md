# Fábrica de Desarrollo con Agentes IA

Este repositorio contiene una **fábrica de desarrollo local** basada en agentes de IA.

- El código de la **fábrica** (orquestador, agentes, Docker, documentación) está en la raíz.
- Una **aplicación de ejemplo generada** por la fábrica está en `apps/prueba-005/`.

La fábrica usa:

- **LangGraph** para orquestar agentes.
- **DeepSeek** a través de OpenRouter como modelo de lenguaje.
- **NestJS** para el backend.
- **Next.js** (App Router) para el frontend.
- **Docker Compose** para la infraestructura local.
- **Qdrant** como base de conocimientos RAG.
- **PostgreSQL** para checkpoints del grafo.

---

## Contenido del repositorio

```text
fabrica-desarrollo-ia/
├── docker-compose.yml         # Infraestructura completa
├── orquestador/               # Código de la fábrica (Python)
│   ├── src/
│   │   ├── main.py            # Punto de entrada
│   │   ├── graph.py           # Grafo LangGraph
│   │   ├── agentes.py         # Nodos y agentes
│   │   ├── models.py          # Configuración de modelos
│   │   ├── rag.py             # Consulta a Qdrant
│   │   └── encargos/          # Encargos de prueba
│   └── Dockerfile
├── sandbox/                   # Contenedor Node.js para validar código
│   └── Dockerfile
├── docs/                      # Documentación del proyecto
└── apps/prueba-005/           # Aplicación generada de ejemplo
    ├── backend/               # NestJS (puerto 3001)
    └── frontend/              # Next.js (puerto 3000)
```

---

## Requisitos previos

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) o Docker Engine + Docker Compose.
- [Git](https://git-scm.com/).
- Cuenta en [GitHub](https://github.com/).
- Cuenta en [OpenRouter](https://openrouter.ai/) con crédito disponible.
- Token de GitHub con permisos para crear repositorios en la organización configurada.

---

## Configuración inicial

1. Clonar el repositorio:

```bash
git clone https://github.com/adn-fabrica-lab/fabrica-desarrollo-ia.git
cd fabrica-desarrollo-ia
```

2. Crear el archivo `.env` en la raíz con al menos estas variables:

```bash
OPENROUTER_API_KEY=sk-or-v1-...
GITHUB_USER=TuUsuarioGithub
GITHUB_TOKEN=ghp_...
GITHUB_ORG=adn-fabrica-lab
```

3. (Opcional pero recomendado) Cargar documentación RAG en Qdrant:

```bash
docker compose up -d
docker compose exec orquestador python src/cargar_rag.py
```

---

## Cómo ejecutar la fábrica

Levantar toda la infraestructura:

```bash
docker compose up -d
```

Ejecutar un encargo (por defecto `src/encargos/prueba-005.md`):

```bash
docker compose exec orquestador python src/main.py
```

Para usar otro encargo:

```bash
docker compose exec orquestador python src/main.py src/encargos/otro-encargo.md
```

El proceso pedirá aprobación humana en dos checkpoints:

1. Aprobación del plan técnico del arquitecto.
2. Aprobación del resultado final antes de publicar la rama en GitHub.

Si la corrida se interrumpe, se puede retomar con:

```bash
docker compose exec orquestador python src/main.py --thread <thread_id>
```

El `thread_id` se muestra al iniciar cada corrida.

---

## Cómo correr la aplicación de ejemplo (`apps/prueba-005`)

La carpeta `apps/prueba-005` contiene una aplicación de lista de tareas generada por la fábrica.

### 1. Backend

```bash
cd apps/prueba-005/backend
npm install
npm run start
```

El backend escucha en `http://localhost:3001`.

Endpoints:

- `GET /tareas?prioridad=alta|media|baja`
- `POST /tareas`
- `PATCH /tareas/:id/completar`
- `DELETE /tareas/:id`

### 2. Frontend

En otra terminal:

```bash
cd apps/prueba-005/frontend
npm install
npm run dev
```

Abrir `http://localhost:3000` en el navegador.

El frontend usa la variable `NEXT_PUBLIC_API_URL` definida en `apps/prueba-005/frontend/.env.local` para conectarse al backend.

---

## Cómo crear un nuevo encargo

1. Crear un archivo Markdown en `orquestador/src/encargos/` describiendo la aplicación deseada.
2. Ejecutar:

```bash
docker compose exec orquestador python src/main.py src/encargos/nuevo-encargo.md
```

3. Aprobar los checkpoints humanos.
4. El agente de repositorio publicará el resultado en un nuevo repositorio bajo la organización configurada.

---

## Solución de problemas

### No se puede conectar al backend desde el frontend

Verifica que el archivo `apps/prueba-005/frontend/.env.local` contenga:

```text
NEXT_PUBLIC_API_URL=http://localhost:3001
```

### El push a GitHub falla

Asegúrate de que `GITHUB_TOKEN` tenga permisos para crear repositorios en `GITHUB_ORG`.

### Qdrant no responde

Verifica que el contenedor esté levantado:

```bash
docker compose ps
```

---

## Licencia

Uso interno de ADN Fábrica Lab.
