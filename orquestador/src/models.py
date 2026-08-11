# orquestador/src/models.py
import os

from langchain_openai import ChatOpenAI

# Modelo asignado por agente (S5 y S11 del plan). Se puede cambiar sin tocar
# codigo definiendo una variable de entorno en .env, por ejemplo:
#   MODELO_ARQUITECTO=deepseek/deepseek-r1
# Todos los roles usan DeepSeek por defecto; los roles que requieren mayor
# razonamiento (arquitecto, revisor) usan el modelo razonador (R1), mientras
# que los demas usan deepseek-chat.
MODELOS_POR_ROL = {
    "coordinador": "deepseek/deepseek-chat",
    "arquitecto": "deepseek/deepseek-r1",
    "backend": "deepseek/deepseek-chat",
    "frontend": "deepseek/deepseek-chat",
    "integrador": "deepseek/deepseek-chat",
    "revisor": "deepseek/deepseek-r1",
}

# Leccion de la Fase 1: sin este limite, algunos modelos piden hasta 64000
# tokens de salida por defecto y OpenRouter rechaza la peticion con 402 si el
# saldo de la key no alcanza a cubrir ese maximo teorico, aunque la respuesta
# real sea corta. En la Fase 2 el default sube a 8000 porque cada programador
# devuelve un proyecto completo en una sola respuesta JSON. Ajustable sin
# tocar codigo definiendo MAX_TOKENS_SALIDA en .env.
MAX_TOKENS_SALIDA = int(os.environ.get("MAX_TOKENS_SALIDA", "8000"))


def obtener_modelo(rol: str) -> ChatOpenAI:
    nombre = os.environ.get("MODELO_" + rol.upper()) or MODELOS_POR_ROL[rol]
    return ChatOpenAI(
        model=nombre,
        api_key=os.environ["OPENROUTER_API_KEY"],
        base_url="https://openrouter.ai/api/v1",
        temperature=0,
        max_tokens=MAX_TOKENS_SALIDA,
    )
