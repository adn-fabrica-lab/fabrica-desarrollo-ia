# orquestador/src/probar_rag.py
from rag import consultar_rag

PRUEBAS = [
    ("backend", "How to enable CORS in a NestJS application"),
    ("frontend", "How to fetch data in a Next.js App Router page"),
]

for area, consulta in PRUEBAS:
    fragmentos = consultar_rag(consulta, area, limite=2)
    print(area + ": " + str(len(fragmentos)) + " fragmentos recuperados")
    if fragmentos:
        print("   Muestra: " + fragmentos[0][:200].replace("\n", " ") + "...")
