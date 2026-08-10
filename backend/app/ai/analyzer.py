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

    ticket.ai_category = data["categoria"]
    ticket.ai_priority = data["prioridad"]
    ticket.ai_summary = data["resumen"]
    ticket.ai_response = data["respuesta"]

    return data