# orquestador/src/main.py
import sys
from datetime import datetime

from dotenv import load_dotenv
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.types import Command

from graph import construir_grafo, obtener_db_uri

load_dotenv()


def preguntar_al_humano(peticion: dict) -> dict:
    print()
    print("=" * 60)
    print("CHECKPOINT HUMANO: " + peticion.get("titulo", ""))
    print("=" * 60)
    print(peticion.get("detalle", ""))
    print()
    respuesta = ""
    while respuesta not in ("s", "n"):
        respuesta = input("Apruebas? (s/n): ").strip().lower()
    if respuesta == "s":
        return {"aprobado": True, "comentarios": ""}
    comentarios = input("Comentarios para la correccion: ").strip()
    return {"aprobado": False, "comentarios": comentarios}


if __name__ == "__main__":
    # Uso:
    #   python src/main.py [ruta_encargo]        -> corrida nueva
    #   python src/main.py --thread <thread_id>  -> retomar una corrida pausada
    args = sys.argv[1:]
    thread_a_retomar = None
    ruta_encargo = "src/encargos/prueba-005.md"
    if len(args) >= 2 and args[0] == "--thread":
        thread_a_retomar = args[1]
    elif len(args) >= 1:
        ruta_encargo = args[0]

    db_uri = obtener_db_uri()

    with PostgresSaver.from_conn_string(db_uri) as checkpointer:
        checkpointer.setup()
        grafo = construir_grafo(checkpointer)

        if thread_a_retomar:
            # NUEVO Fase 5: retomar un thread pausado exactamente donde quedo.
            thread_id = thread_a_retomar
            print("Retomando thread:", thread_id)
            config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 60,
            }
            estado = grafo.get_state(config)
            if not estado.next:
                print("Ese thread no tiene pasos pendientes (ya termino o no existe).")
                sys.exit(1)
            interrupciones = [
                i for t in estado.tasks for i in (t.interrupts or [])
            ]
            if interrupciones:
                datos = preguntar_al_humano(interrupciones[0].value)
                resultado = grafo.invoke(Command(resume=datos), config=config)
            else:
                # El thread quedo pausado por una excepcion no controlada
                # (por ejemplo, git push fallo). Re-ejecutamos desde el ultimo
                # checkpoint disponible para retomar el nodo que fallo.
                print("Retomando desde el ultimo checkpoint (no es un checkpoint humano)...")
                resultado = grafo.invoke(None, config=config)
        else:
            with open(ruta_encargo, "r", encoding="utf-8") as f:
                texto = f.read()
            # Un thread_id nuevo por corrida (anotalo en la bitacora: es la
            # llave para retomar la corrida si algo la interrumpe).
            thread_id = "fase5-" + datetime.now().strftime("%Y%m%d-%H%M%S")
            print("Thread:", thread_id)
            config = {
                "configurable": {"thread_id": thread_id},
                "recursion_limit": 60,
            }
            resultado = grafo.invoke(
                {"encargo": {"texto_original": texto}, "ciclo": 0},
                config=config,
            )

        while resultado.get("__interrupt__"):
            peticion = resultado["__interrupt__"][0].value
            datos = preguntar_al_humano(peticion)
            resultado = grafo.invoke(Command(resume=datos), config=config)

    print()
    print("=== Resultado final ===")
    print("Encargo:           ", resultado.get("encargo_id"))
    print("Rama publicada:    ", resultado.get("rama_git"))
    print("Ciclos usados:     ", resultado.get("ciclo"))
    print("Hallazgos finales: ", len(resultado.get("hallazgos_revision") or []))
    for area, pasos in (resultado.get("resultado_sandbox") or {}).items():
        for paso, res in pasos.items():
            print("Sandbox " + area + " " + paso + ":", "OK" if res.get("ok") else "FALLO")
