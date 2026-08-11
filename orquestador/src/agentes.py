# orquestador/src/agentes.py
import json
import os
import re
import shutil
import subprocess

from langgraph.types import interrupt
from models import obtener_modelo
from rag import consultar_rag
from state import EstadoFabricaDesarrollo

RUTA_TRABAJO = "/app/workspace"
RUTA_SANDBOX = "/sandbox-workspace"  # mismo volumen que /workspace del sandbox
CONTENEDOR_SANDBOX = "fabrica_sandbox"
TOPE_CICLOS = 3


def _limpiar_json(texto: str) -> str:
    # El modelo a veces envuelve el JSON en texto o en un bloque de codigo,
    # o agrega texto despues del JSON valido. raw_decode parsea el primer
    # objeto JSON completo y descarta el resto, evitando errores por texto
    # sobrante.
    inicio = texto.find("{")
    if inicio == -1:
        raise ValueError("El modelo no devolvio JSON. Respuesta: " + texto[:300])
    return texto[inicio:]


def _corregir_escapes_json(texto: str) -> str:
    # El modelo a veces escribe escapes invalidos como "\." en regex de
    # package.json. Esta funcion duplica la barra invertida cuando no es
    # un escape JSON valido (", \, /, b, f, n, r, t, u).
    return re.sub(r"\\([^\"\\\\/bfnrtu])", r"\\\\\\1", texto)


def _sanitizar_package_json(ruta: str) -> None:
    # Asegura que package.json sea JSON valido antes de npm install. Si el
    # modelo genero escapes invalidos, intenta corregirlos automaticamente.
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            contenido = f.read()
        json.loads(contenido)
        return
    except (OSError, json.JSONDecodeError):
        pass
    try:
        contenido = _corregir_escapes_json(contenido)
        json.loads(contenido)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(contenido)
        print("   Corregido package.json con escapes JSON invalidos")
    except Exception:
        pass


def _asegurar_nestjs_testing(ruta_pkg: str, ruta_area: str) -> None:
    # Parche de robustez: si hay archivos .spec.ts y package.json no trae
    # @nestjs/testing, agregarlo para que las pruebas unitarias de NestJS
    # no fallen por dependencia faltante.
    if not os.path.exists(ruta_pkg):
        return
    try:
        with open(ruta_pkg, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return
    tiene_specs = any(
        nombre.endswith(".spec.ts")
        for _, _, archivos in os.walk(ruta_area)
        for nombre in archivos
    )
    if not tiene_specs:
        return
    dev = pkg.setdefault("devDependencies", {})
    if "@nestjs/testing" not in dev:
        dev["@nestjs/testing"] = "^10.0.0"
        with open(ruta_pkg, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2, ensure_ascii=False)
        print("   Agregado @nestjs/testing a devDependencies")


def _quitar_lint_frontend(ruta_pkg: str) -> None:
    # El encargo prueba-005 (y otros similares) especifica que el frontend no
    # debe tener script 'lint'. Si el modelo lo agrego, lo removemos para
    # evitar que falle el paso de lint en el sandbox.
    if not os.path.exists(ruta_pkg):
        return
    try:
        with open(ruta_pkg, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return
    if "scripts" in pkg and "lint" in pkg["scripts"]:
        del pkg["scripts"]["lint"]
        with open(ruta_pkg, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2, ensure_ascii=False)
        print("   Removido script 'lint' del frontend")


def _normalizar_package_nestjs(ruta_pkg: str) -> None:
    # Parches de robustez para package.json de backend NestJS. El modelo a
    # veces inventa versiones inexistentes u omite dependencias obligatorias.
    if not os.path.exists(ruta_pkg):
        return
    try:
        with open(ruta_pkg, "r", encoding="utf-8") as f:
            pkg = json.load(f)
    except (OSError, json.JSONDecodeError):
        return
    cambios = False

    deps = pkg.setdefault("dependencies", {})
    if "@nestjs/platform-express" not in deps:
        deps["@nestjs/platform-express"] = "^10.0.0"
        cambios = True

    dev = pkg.setdefault("devDependencies", {})
    version_jest = dev.get("@types/jest", "")
    if version_jest.startswith("^29.7") or version_jest.startswith("29.7"):
        # @types/jest no tiene versiones 29.7.x; la ultima estable 29.x es 29.5.14
        dev["@types/jest"] = "^29.5.14"
        cambios = True

    if cambios:
        with open(ruta_pkg, "w", encoding="utf-8") as f:
            json.dump(pkg, f, indent=2, ensure_ascii=False)
        print("   Normalizadas dependencias de NestJS en package.json")


def _normalizar_env_local(ruta_env: str) -> None:
    # El frontend de Next.js usa NEXT_PUBLIC_API_URL para saber donde esta el
    # backend. El encargo fija el backend en el puerto 3001; si el modelo trunca
    # la URL, corregimos a http://localhost:3001.
    if not os.path.exists(ruta_env):
        return
    try:
        with open(ruta_env, "r", encoding="utf-8") as f:
            contenido = f.read()
    except OSError:
        return
    nuevo = re.sub(
        r"NEXT_PUBLIC_API_URL\s*=\s*http://localhost:300(?!1)",
        "NEXT_PUBLIC_API_URL=http://localhost:3001",
        contenido,
    )
    if nuevo != contenido:
        with open(ruta_env, "w", encoding="utf-8") as f:
            f.write(nuevo)
        print("   Corregida NEXT_PUBLIC_API_URL a http://localhost:3001")


def _pedir_json(rol: str, instrucciones: str, contenido: str, intentos: int = 3) -> dict:
    modelo = obtener_modelo(rol)
    ultimo_error = None
    for intento in range(1, intentos + 1):
        mensajes = [
            (
                "system",
                instrucciones
                + " Responde UNICAMENTE con un objeto JSON valido, sin explicaciones.",
            ),
            ("user", contenido),
        ]
        if ultimo_error is not None:
            mensajes.append((
                "user",
                "Tu respuesta anterior no era JSON valido (error: " + str(ultimo_error) +
                "). Responde de nuevo UNICAMENTE con un objeto JSON valido y completo, sin explicaciones ni texto adicional.",
            ))
        try:
            respuesta = modelo.invoke(mensajes)
            texto_limpio = _limpiar_json(respuesta.content)
            objeto, _ = json.JSONDecoder().raw_decode(texto_limpio)
            return objeto
        except (ValueError, json.JSONDecodeError) as error:
            ultimo_error = error
            if intento == intentos:
                raise
    raise ultimo_error


def _graves(hallazgos, area=None):
    # Filtra hallazgos de severidad alta, opcionalmente por area.
    resultado = []
    for h in hallazgos or []:
        if h.get("severidad") != "alta":
            continue
        if area is None or h.get("area") == area:
            resultado.append(h)
    return resultado


def _rutas_afectadas(hallazgos) -> set:
    # rutas de archivo senaladas por los hallazgos (si las traen).
    rutas = set()
    for h in hallazgos or []:
        if h.get("ruta"):
            rutas.add(h["ruta"])
    return rutas


def nodo_coordinador(estado: EstadoFabricaDesarrollo) -> dict:
    print("1. Coordinador: interpretando el encargo...")
    datos = _pedir_json(
        "coordinador",
        "Eres el Coordinador de una fabrica de desarrollo de software. "
        "Extrae del encargo un JSON con esta forma exacta: "
        '{"encargo_id": "...", "repositorio": "...", "titulo": "...", '
        '"descripcion": "...", "criterios": ["..."]}. '
        "El repositorio viene indicado en el encargo; nunca lo inventes.",
        estado["encargo"]["texto_original"],
    )
    encargo = dict(estado["encargo"])
    encargo.update(datos)
    return {"encargo": encargo, "encargo_id": datos["encargo_id"]}


def nodo_arquitecto(estado: EstadoFabricaDesarrollo) -> dict:
    print("2. Arquitecto: disenando el plan tecnico (backend + frontend)...")
    consulta = (
        (estado["encargo"].get("titulo") or "")
        + " "
        + (estado["encargo"].get("descripcion") or "")
    )
    contexto = {
        "encargo": estado["encargo"],
        "documentacion": consultar_rag(consulta, "ambas", limite=2),
        # NUEVO Fase 4: si un humano rechazo el plan o el resultado final,
        # sus comentarios y el plan anterior viajan como contexto.
        "comentarios_de_revision_humana": estado.get("comentarios_humanos") or "",
        "plan_anterior": estado.get("plan_tecnico") or {},
    }
    plan = _pedir_json(
        "arquitecto",
        "Eres el Arquitecto de Software de una fabrica de desarrollo. "
        "El proyecto tiene un backend NestJS (TypeScript) en la carpeta "
        "backend/ y un frontend Next.js (TypeScript, App Router) en la "
        "carpeta frontend/. A partir del encargo, produce un plan tecnico "
        "JSON con esta forma exacta: "
        '{"resumen": "...", '
        '"contrato_api": [{"metodo": "GET", "ruta": "/...", '
        '"respuesta_ejemplo": {}}], '
        '"archivos_backend": [{"ruta": "backend/...", "accion": "crear", '
        '"descripcion": "..."}], '
        '"archivos_frontend": [{"ruta": "frontend/...", "accion": "crear", '
        '"descripcion": "..."}]}. '
        "El contrato_api es la unica fuente de verdad de los endpoints: "
        "backend y frontend deben implementarlo tal cual. Incluye TODOS los "
        "archivos necesarios para que cada proyecto sea completo e instalable "
        "(package.json con script build, tsconfig.json, src/..., app/...). "
        "Si los criterios piden pruebas unitarias, incluye los archivos "
        ".spec.ts correspondientes en archivos_backend. Escribe cada "
        "descripcion de archivo de forma especifica y completa: sera la "
        "unica guia que tendra el programador al escribir ese archivo. "
        "documentacion trae fragmentos de la documentacion oficial: apoyate "
        "en ella. Manten el plan lo mas pequeno posible cumpliendo el "
        "encargo. Si comentarios_de_revision_humana no esta vacio, un "
        "humano rechazo la propuesta anterior (plan_anterior): produce un "
        "plan corregido que atienda esos comentarios al pie de la letra.",
        json.dumps(contexto, ensure_ascii=False),
    )
    # Fase 4: la aprobacion ya no es automatica; la decide el humano en el
    # nodo checkpoint_plan.
    return {"plan_tecnico": plan}


def _programar_por_archivos(area: str, estado: EstadoFabricaDesarrollo) -> list[dict]:
    # Patron "plan por archivo" (S6 del plan): una llamada al
    # modelo POR ARCHIVO con contexto acotado, en vez de pedir el proyecto
    # completo en una sola respuesta gigante (que en la Fase 2 rozaba el tope
    # de tokens y podia truncar el JSON).
    plan = estado["plan_tecnico"]
    archivos_del_plan = plan.get("archivos_" + area) or []
    actuales = {
        a["ruta"]: a["contenido"] for a in (estado.get("archivos_" + area) or [])
    }
    graves = _graves(estado.get("hallazgos_revision"), area)
    correccion = bool(actuales) and bool(graves)
    rutas_a_corregir = _rutas_afectadas(graves)

    if area == "backend":
        rol_descripcion = "Programador Backend (NestJS + TypeScript)"
    else:
        rol_descripcion = "Programador Frontend (Next.js + TypeScript, App Router)"

    resultado = []
    for archivo in archivos_del_plan:
        ruta = archivo["ruta"]
        # En una correccion solo se reescriben los archivos senalados por los
        # hallazgos; si ningun hallazgo trae ruta, se reescribe todo el area.
        if correccion and rutas_a_corregir and ruta not in rutas_a_corregir:
            if ruta in actuales:
                resultado.append({"ruta": ruta, "contenido": actuales[ruta]})
                continue
        print("   Escribiendo " + ruta + "...")
        contexto = {
            "criterios_del_encargo": estado["encargo"].get("criterios"),
            "resumen_plan": plan.get("resumen"),
            "contrato_api": plan.get("contrato_api"),
            "rutas_de_todo_el_plan": [a.get("ruta") for a in archivos_del_plan],
            "archivo_a_escribir": archivo,
            "contenido_actual": actuales.get(ruta),
            "otros_archivos_del_area": {
                k: v for k, v in actuales.items() if k != ruta
            },
            "hallazgos_a_corregir": [
                h for h in graves if h.get("ruta") in (None, "", ruta)
            ],
            "documentacion": consultar_rag(
                (archivo.get("descripcion") or "") + " " + ruta, area, limite=2
            ),
        }
        instrucciones_backend = (
            "Eres el Programador Backend (NestJS + TypeScript). Escribe el "
            "contenido COMPLETO de UN SOLO archivo: el indicado en "
            "archivo_a_escribir. Debe ser coherente con contrato_api y con "
            "rutas_de_todo_el_plan (los imports entre archivos deben "
            "corresponder a esas rutas). otros_archivos_del_area trae el "
            "contenido actual del resto del backend: usa esos nombres de "
            "metodos, firmas y tipos exactamente (service, controller y tests "
            "deben coincidir). Define los tipos localmente si no hay un "
            "archivo de tipos separado. Convierte a numero los ids que llegan "
            "como string en el controlador. Los metodos completarTarea y "
            "eliminarTarea deben lanzar un error 'Tarea no encontrada' cuando "
            "el id no exista. documentacion trae fragmentos de la "
            "documentacion oficial de NestJS: sigue sus patrones y convenciones. "
            "Si hallazgos_a_corregir tiene elementos, corrige esos problemas "
            "partiendo de contenido_actual. Si el archivo es package.json, "
            "incluye @nestjs/platform-express en dependencies, "
            "@nestjs/testing en devDependencies cuando exista algun "
            ".spec.ts, y usa versiones reales publicadas: "
            "@types/jest ^29.5.14 (NO ^29.7.0, no existe), jest ^29.7.0, "
            "@types/node ^20.11.0, @types/express ^4.17.21. "
            "Asegurate de que cualquier regex JSON use doble barra invertida "
            "(\\\\.) para escapes validos. "
            "Responde JSON con esta forma exacta: "
            '{"contenido": "..."}.'
        )
        instrucciones_frontend = (
            "Eres el Programador Frontend (Next.js + TypeScript, App Router). "
            "Escribe el contenido COMPLETO de UN SOLO archivo: el indicado en "
            "archivo_a_escribir. Debe ser coherente con contrato_api y con "
            "rutas_de_todo_el_plan. documentacion trae fragmentos de la "
            "documentacion oficial de Next.js: sigue sus patrones y "
            "convenciones. Si hallazgos_a_corregir tiene elementos, corrige "
            "esos problemas partiendo de contenido_actual. Si el archivo es "
            "package.json, NO definas un script 'lint' e incluye scripts "
            "'dev', 'build' y 'start'. Si el archivo es .env.local, define "
            "EXACTAMENTE NEXT_PUBLIC_API_URL=http://localhost:3001 (el backend "
            "corre en el puerto 3001). Usa versiones publicadas y estables; "
            "ante la duda usa un rango amplio. "
            "Responde JSON con esta forma exacta: "
            '{"contenido": "..."}.'
        )
        instrucciones = instrucciones_backend if area == "backend" else instrucciones_frontend
        datos = _pedir_json(
            area,
            instrucciones,
            json.dumps(contexto, ensure_ascii=False),
        )
        resultado.append({"ruta": ruta, "contenido": datos["contenido"]})
    return resultado


def nodo_programador_backend(estado: EstadoFabricaDesarrollo) -> dict:
    print("3. Programador Backend: escribiendo NestJS archivo por archivo...")
    return {"archivos_backend": _programar_por_archivos("backend", estado)}


def decidir_despues_de_backend(estado: EstadoFabricaDesarrollo) -> str:
    if not (estado.get("archivos_frontend") or []):
        # Primera pasada: el frontend aun no existe.
        return "frontend"
    if _graves(estado.get("hallazgos_revision"), "frontend"):
        # Tambien hay correcciones de frontend pendientes en este ciclo.
        return "frontend"
    # Correccion solo de backend: pasar directo a re-verificar contratos,
    # sin re-ejecutar (ni re-pagar) el nodo Frontend.
    return "integrador"


def nodo_programador_frontend(estado: EstadoFabricaDesarrollo) -> dict:
    print("4. Programador Frontend: escribiendo Next.js archivo por archivo...")
    return {"archivos_frontend": _programar_por_archivos("frontend", estado)}


def nodo_integrador(estado: EstadoFabricaDesarrollo) -> dict:
    print("5. Integrador: verificando contratos entre backend y frontend...")
    contexto = {
        "contrato_api": estado["plan_tecnico"].get("contrato_api"),
        "archivos_backend": estado["archivos_backend"],
        "archivos_frontend": estado["archivos_frontend"],
    }
    datos = _pedir_json(
        "integrador",
        "Eres el Integrador. Verifica que el backend implemente el "
        "contrato_api tal cual (metodos, rutas, forma del JSON, puerto) y que "
        "el frontend consuma exactamente esos mismos endpoints y formas. "
        "Responde JSON con esta forma exacta: "
        '{"hallazgos": [{"area": "backend", "ruta": "...", "detalle": "...", '
        '"severidad": "alta"}]}. '
        'area es "backend" o "frontend" segun donde deba corregirse. Usa una '
        "lista vacia si los contratos coinciden. Reporta solo "
        "incompatibilidades reales, no mejoras opcionales.",
        json.dumps(contexto, ensure_ascii=False),
    )
    return {"hallazgos_integracion": datos["hallazgos"]}


def _correr_paso(carpeta: str, comando: str) -> dict:
    try:
        proceso = subprocess.run(
            [
                "docker", "exec", CONTENEDOR_SANDBOX, "sh", "-lc",
                "cd /workspace/" + carpeta + " && " + comando,
            ],
            capture_output=True,
            text=True,
            timeout=900,
        )
    except subprocess.TimeoutExpired:
        return {"ok": False, "salida_final": "Timeout: el paso supero los 15 minutos."}
    salida = (proceso.stdout + "\n" + proceso.stderr).strip()
    # Solo se conserva el final de la salida: ahi esta el error si lo hay.
    return {"ok": proceso.returncode == 0, "salida_final": salida[-2000:]}


def _scripts_npm(carpeta: str) -> dict:
    # Lee los scripts del package.json directo del volumen compartido.
    ruta = os.path.join(RUTA_SANDBOX, carpeta, "package.json")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            return json.load(f).get("scripts") or {}
    except (OSError, ValueError):
        return {}


def _correr_en_sandbox(carpeta: str) -> dict:
    # Cada paso se corre y reporta POR SEPARADO (leccion de la
    # Fase 2: el install encadenado con --silent escondia la causa real).
    # test y lint solo corren si el proyecto define esos scripts.
    resultado = {
        "install": _correr_paso(carpeta, "npm install --no-audit --no-fund --silent")
    }
    if not resultado["install"]["ok"]:
        return resultado
    resultado["build"] = _correr_paso(carpeta, "npm run build")
    scripts = _scripts_npm(carpeta)
    if "test" in scripts:
        resultado["test"] = _correr_paso(carpeta, "npm test -- --passWithNoTests")
    if "lint" in scripts:
        resultado["lint"] = _correr_paso(carpeta, "npm run lint")
    return resultado


def nodo_sandbox(estado: EstadoFabricaDesarrollo) -> dict:
    print("6. Sandbox: install + build + test + lint reales (puede tardar)...")
    raiz = os.path.join(RUTA_SANDBOX, estado["encargo_id"])
    # Igual que en la Fase 2: no se borra la carpeta (node_modules en cache);
    # los archivos fuente se sobreescriben con la version mas reciente.
    for archivo in (estado["archivos_backend"] or []) + (
        estado.get("archivos_frontend") or []
    ):
        ruta = os.path.join(raiz, archivo["ruta"])
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(archivo["contenido"])

    resultado = {}
    for area in ("backend", "frontend"):
        if os.path.isdir(os.path.join(raiz, area)):
            ruta_pkg = os.path.join(raiz, area, "package.json")
            ruta_area = os.path.join(raiz, area)
            _sanitizar_package_json(ruta_pkg)
            if area == "backend":
                _asegurar_nestjs_testing(ruta_pkg, ruta_area)
                _normalizar_package_nestjs(ruta_pkg)
            if area == "frontend":
                _quitar_lint_frontend(ruta_pkg)
                _normalizar_env_local(os.path.join(ruta_area, ".env.local"))
            print("   Verificando " + area + "...")
            pasos = _correr_en_sandbox(estado["encargo_id"] + "/" + area)
            resultado[area] = pasos
            for paso, res in pasos.items():
                print("   " + area + " " + paso + ": " + ("OK" if res["ok"] else "FALLO"))
    return {"resultado_sandbox": resultado}


def nodo_revisor(estado: EstadoFabricaDesarrollo) -> dict:
    ciclo = estado.get("ciclo", 0) + 1
    print("7. Revisor: consolidando la revision (ciclo " + str(ciclo) + ")...")
    contexto = {
        "encargo": estado["encargo"],
        "plan_tecnico": estado["plan_tecnico"],
        "archivos_backend": estado["archivos_backend"],
        "archivos_frontend": estado.get("archivos_frontend") or [],
        "hallazgos_integracion": estado.get("hallazgos_integracion") or [],
        "resultado_sandbox": estado.get("resultado_sandbox") or {},
    }
    datos = _pedir_json(
        "revisor",
        "Eres el Revisor de Codigo. Consolida la revision final con tres "
        "insumos: (1) el codigo debe cumplir el encargo y el plan tecnico; "
        "(2) hallazgos_integracion trae incompatibilidades de contrato ya "
        "detectadas por el Integrador; (3) resultado_sandbox trae por "
        "proyecto el resultado REAL de install, build, test y lint. Si "
        "install, build o test tienen ok en false, ese fallo es "
        "obligatoriamente un hallazgo de severidad alta (usa salida_final "
        "para diagnosticar la causa e indica en ruta el archivo exacto a "
        "corregir). Si lint tiene ok en false, registralo como severidad "
        "media. Responde JSON con esta forma exacta: "
        '{"hallazgos": [{"area": "backend", "ruta": "...", "detalle": "...", '
        '"severidad": "alta"}]}. area es "backend" o "frontend". La '
        'severidad es "alta", "media" o "baja". Usa una lista vacia si todo '
        "esta bien. Reporta solo problemas reales que impidan cumplir el "
        "encargo.",
        json.dumps(contexto, ensure_ascii=False),
    )
    return {"hallazgos_revision": datos["hallazgos"], "ciclo": ciclo}


def decidir_despues_de_revision(estado: EstadoFabricaDesarrollo) -> str:
    graves_back = _graves(estado.get("hallazgos_revision"), "backend")
    graves_front = _graves(estado.get("hallazgos_revision"), "frontend")
    if (graves_back or graves_front) and estado.get("ciclo", 0) < TOPE_CICLOS:
        if graves_back:
            print(
                "   Revisor: "
                + str(len(graves_back))
                + " hallazgos graves de backend. Vuelve al Backend."
            )
            return "backend"
        print(
            "   Revisor: "
            + str(len(graves_front))
            + " hallazgos graves de frontend. Vuelve al Frontend."
        )
        return "frontend"
    if graves_back or graves_front:
        print("   Revisor: aun hay hallazgos, pero se alcanzo el tope de ciclos.")
    return "repositorio"


def nodo_repositorio(estado: EstadoFabricaDesarrollo) -> dict:
    print("8. Agente de Repositorio: publicando el codigo en una rama...")
    org = os.environ["GITHUB_ORG"]
    usuario = os.environ["GITHUB_USER"]
    token = os.environ["GITHUB_TOKEN"]
    repo = estado["encargo"]["repositorio"]
    rama = "encargo/" + estado["encargo_id"]
    url = "https://" + usuario + ":" + token + "@github.com/" + org + "/" + repo + ".git"
    destino = os.path.join(RUTA_TRABAJO, repo)

    if os.path.exists(destino):
        shutil.rmtree(destino)
    os.makedirs(RUTA_TRABAJO, exist_ok=True)
    subprocess.run(["git", "clone", url, destino], check=True)
    subprocess.run(["git", "checkout", "-b", rama], cwd=destino, check=True)

    archivos = (estado["archivos_backend"] or []) + (
        estado.get("archivos_frontend") or []
    )
    for archivo in archivos:
        ruta = os.path.join(destino, archivo["ruta"])
        os.makedirs(os.path.dirname(ruta), exist_ok=True)
        with open(ruta, "w", encoding="utf-8") as f:
            f.write(archivo["contenido"])

    mensaje = "Encargo " + estado["encargo_id"] + ": " + estado["encargo"].get("titulo", "")
    subprocess.run(["git", "add", "."], cwd=destino, check=True)
    subprocess.run(
        [
            "git",
            "-c", "user.name=Fabrica de Desarrollo",
            "-c", "user.email=fabrica@adn.local",
            "commit", "-m", mensaje,
        ],
        cwd=destino,
        check=True,
    )
    # Fuerza el push porque la rama es generada automaticamente; si una
    # corrida anterior dejo la rama remota por delante, un push normal fallaria.
    subprocess.run(
        ["git", "push", "-u", "origin", rama, "--force"],
        cwd=destino,
        check=True,
    )
    print("   Rama publicada: " + rama)
    return {"rama_git": rama}


# --- NUEVO Fase 4: checkpoints humanos por terminal (S10 del plan) ---
# Nota importante: cuando el humano responde, LangGraph RE-EJECUTA el nodo
# que contiene interrupt() desde su inicio. Por eso estos nodos solo arman
# un resumen y preguntan: sin llamadas al LLM ni efectos secundarios.


def _resumen_plan_para_humano(estado: EstadoFabricaDesarrollo) -> str:
    plan = estado["plan_tecnico"]
    lineas = ["Resumen: " + str(plan.get("resumen", ""))]
    lineas.append("Contrato API:")
    for e in plan.get("contrato_api") or []:
        lineas.append("  - " + str(e.get("metodo")) + " " + str(e.get("ruta")))
    lineas.append("Archivos backend:")
    for a in plan.get("archivos_backend") or []:
        lineas.append("  - " + str(a.get("ruta")))
    lineas.append("Archivos frontend:")
    for a in plan.get("archivos_frontend") or []:
        lineas.append("  - " + str(a.get("ruta")))
    return "\n".join(lineas)


def nodo_checkpoint_plan(estado: EstadoFabricaDesarrollo) -> dict:
    respuesta = interrupt({
        "titulo": "Aprobar el plan del Arquitecto",
        "detalle": _resumen_plan_para_humano(estado),
    })
    aprobado = bool(respuesta.get("aprobado"))
    return {
        "plan_aprobado": aprobado,
        "comentarios_humanos": respuesta.get("comentarios") or "",
    }


def decidir_despues_de_checkpoint_plan(estado: EstadoFabricaDesarrollo) -> str:
    if estado.get("plan_aprobado"):
        print("   Plan aprobado por el humano. A programar.")
        return "backend"
    print("   Plan rechazado. Vuelve al Arquitecto con tus comentarios.")
    return "arquitecto"


def _archivos_faltantes_del_plan(estado: EstadoFabricaDesarrollo) -> list[str]:
    # NUEVO Fase 5: compara los archivos del plan contra el disco real.
    # RUTA_SANDBOX es la misma constante que usa nodo_sandbox desde la Fase 2.
    plan = estado.get("plan_tecnico") or {}
    base = os.path.join(RUTA_SANDBOX, str(estado.get("encargo_id") or ""))
    faltantes = []
    for clave in ("archivos_backend", "archivos_frontend"):
        for archivo in plan.get(clave) or []:
            ruta = str(archivo.get("ruta") or "")
            if ruta and not os.path.exists(os.path.join(base, ruta)):
                faltantes.append(ruta)
    return faltantes


def _resumen_final_para_humano(estado: EstadoFabricaDesarrollo) -> str:
    lineas = ["Ciclos usados: " + str(estado.get("ciclo"))]
    hallazgos = estado.get("hallazgos_revision") or []
    lineas.append("Hallazgos pendientes (opiniones del Revisor): " + str(len(hallazgos)))
    for h in hallazgos:
        lineas.append(
            "  - [" + str(h.get("severidad")) + "] " + str(h.get("area"))
            + " " + str(h.get("ruta") or "") + ": " + str(h.get("detalle"))[:200]
        )
    for area, pasos in (estado.get("resultado_sandbox") or {}).items():
        for paso, res in pasos.items():
            lineas.append(
                "Sandbox " + area + " " + paso + ": "
                + ("OK" if res.get("ok") else "FALLO")
            )
    # NUEVO Fase 5: verificacion contra el disco. A diferencia de los
    # hallazgos del Revisor (opiniones de un LLM), esta lista es un hecho.
    faltantes = _archivos_faltantes_del_plan(estado)
    if faltantes:
        lineas.append("ATENCION - archivos del plan que NO existen en el workspace:")
        for ruta in faltantes:
            lineas.append("  - " + ruta)
    else:
        lineas.append("Verificacion de archivos: todos los archivos del plan existen.")
    return "\n".join(lineas)

def nodo_checkpoint_final(estado: EstadoFabricaDesarrollo) -> dict:
    respuesta = interrupt({
        "titulo": "Aprobar el resultado antes de publicar la rama",
        "detalle": _resumen_final_para_humano(estado),
    })
    aprobado = bool(respuesta.get("aprobado"))
    if aprobado:
        return {"aprobacion_final": True, "comentarios_humanos": ""}
    # Rechazo: los comentarios van al Arquitecto; se limpian los hallazgos
    # viejos (ya no describen el proximo intento) y el contador de ciclos
    # vuelve a cero para que el nuevo intento tenga su presupuesto completo
    # de correcciones.
    return {
        "aprobacion_final": False,
        "comentarios_humanos": respuesta.get("comentarios") or "",
        "hallazgos_revision": [],
        "ciclo": 0,
    }


def decidir_despues_de_checkpoint_final(estado: EstadoFabricaDesarrollo) -> str:
    if estado.get("aprobacion_final"):
        print("   Resultado aprobado por el humano. Publicando.")
        return "repositorio"
    print("   Resultado rechazado. Vuelve al Arquitecto con tus comentarios.")
    return "arquitecto"
