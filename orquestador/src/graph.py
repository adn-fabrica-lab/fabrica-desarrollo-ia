# orquestador/src/graph.py
import os

from langgraph.graph import StateGraph, END

from state import EstadoFabricaDesarrollo
from agentes import (
    nodo_coordinador,
    nodo_arquitecto,
    nodo_checkpoint_plan,
    nodo_programador_backend,
    nodo_programador_frontend,
    nodo_integrador,
    nodo_sandbox,
    nodo_revisor,
    nodo_checkpoint_final,
    nodo_repositorio,
    decidir_despues_de_checkpoint_plan,
    decidir_despues_de_backend,
    decidir_despues_de_revision,
    decidir_despues_de_checkpoint_final,
)


def obtener_db_uri():
    pg_user = os.environ["POSTGRES_USER"]
    pg_password = os.environ["POSTGRES_PASSWORD"]
    pg_host = os.environ["POSTGRES_HOST"]
    pg_port = os.environ["POSTGRES_PORT"]
    pg_db = os.environ["POSTGRES_DB"]
    return f"postgresql://{pg_user}:{pg_password}@{pg_host}:{pg_port}/{pg_db}"


def construir_grafo(checkpointer):
    # checkpointer debe venir ya abierto (ver main.py): su conexion a Postgres
    # debe seguir viva mientras el grafo se ejecuta. En esta fase tambien
    # sostiene las pausas de los checkpoints humanos.
    builder = StateGraph(EstadoFabricaDesarrollo)

    builder.add_node("coordinador", nodo_coordinador)
    builder.add_node("arquitecto", nodo_arquitecto)
    builder.add_node("checkpoint_plan", nodo_checkpoint_plan)
    builder.add_node("backend", nodo_programador_backend)
    builder.add_node("frontend", nodo_programador_frontend)
    builder.add_node("integrador", nodo_integrador)
    builder.add_node("sandbox", nodo_sandbox)
    builder.add_node("revisor", nodo_revisor)
    builder.add_node("checkpoint_final", nodo_checkpoint_final)
    builder.add_node("repositorio", nodo_repositorio)

    builder.set_entry_point("coordinador")
    builder.add_edge("coordinador", "arquitecto")
    builder.add_edge("arquitecto", "checkpoint_plan")
    builder.add_conditional_edges(
        "checkpoint_plan",
        decidir_despues_de_checkpoint_plan,
        {"backend": "backend", "arquitecto": "arquitecto"},
    )
    builder.add_conditional_edges(
        "backend",
        decidir_despues_de_backend,
        {"frontend": "frontend", "integrador": "integrador"},
    )
    builder.add_edge("frontend", "integrador")
    builder.add_edge("integrador", "sandbox")
    builder.add_edge("sandbox", "revisor")
    builder.add_conditional_edges(
        "revisor",
        decidir_despues_de_revision,
        {
            "backend": "backend",
            "frontend": "frontend",
            # Fase 4: cuando el Revisor da el visto bueno (o se agota el
            # tope de ciclos), ya no se publica directo: primero pasa por
            # el checkpoint humano final.
            "repositorio": "checkpoint_final",
        },
    )
    builder.add_conditional_edges(
        "checkpoint_final",
        decidir_despues_de_checkpoint_final,
        {"repositorio": "repositorio", "arquitecto": "arquitecto"},
    )
    builder.add_edge("repositorio", END)

    return builder.compile(checkpointer=checkpointer)
