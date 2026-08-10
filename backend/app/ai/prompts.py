ANALYZE_TICKET_PROMPT = """
Analiza el siguiente ticket.
En categoria solo poner una de las siguientes opciones: Facturación, Soporte, Ventas.
Devuelve únicamente un JSON válido en español.

Formato:

{{
    "categoria":"",
    "prioridad":"",
    "resumen":"",
    "respuesta":"",
    "sugerencias":""
}}"""