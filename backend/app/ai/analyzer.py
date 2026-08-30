import json
import re

from app.ai.service import ask_ai


def analyze_ticket(ticket):

    prompt = f"""
Analiza el siguiente ticket.
En categoria solo poner una de las siguientes opciones: Facturación, Soporte, Ventas.
En prioridad solo poner una de las siguientes opciones: Baja, Media, Alta, Urgente.
Devuelve únicamente un JSON válido en español.

Formato:

{{
    "categoria":"",
    "prioridad":"",
    "resumen":"",
    "respuesta":"",
    "sugerencias":""
}}

Título:
{ticket.title}

Descripción:
{ticket.description}
"""

    analysis = ask_ai(prompt)

    print("===== RESPUESTA DE OLLAMA =====")
    print(repr(analysis))
    print("===============================")

    if not analysis.strip():
        raise Exception("Ollama devolvió una respuesta vacía")

    # Extraer únicamente el objeto JSON
    match = re.search(r"\{.*\}", analysis, re.DOTALL)

    if not match:
        raise Exception(f"No se encontró un JSON.\nRespuesta:\n{analysis}")

    json_text = match.group()

    print("===== JSON EXTRAÍDO =====")
    print(json_text)
    print("=========================")

    data = json.loads(json_text)

    from app.ai.normalize import normalize_category, normalize_priority

    data["categoria"] = normalize_category(data.get("categoria")).value
    data["prioridad"] = normalize_priority(data.get("prioridad")).value
    return data
